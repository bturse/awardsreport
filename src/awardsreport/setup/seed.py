import argparse
import logging
import requests
from time import sleep
from zipfile import ZipFile
from io import BytesIO
from glob import glob
from typing import Optional
import tempfile
import json
import time
from typing import Any, Mapping

from awardsreport.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

from awardsreport.database import engine
from awardsreport.setup.seed_helpers import (
    get_awards_payloads,
    generate_copy_from_sql,
    USER_AGENT,
    AWARDS_DL_EP,
)


def _sanitize_headers(h: Mapping[str, str]) -> dict[str, str]:
    # You only have User-Agent now, but this prevents future “oops we logged tokens”.
    redacted = {}
    for k, v in h.items():
        if k.lower() in {"authorization", "x-api-key"}:
            redacted[k] = "***REDACTED***"
        else:
            redacted[k] = v
    return redacted


def _payload_for_log(payload_dict: dict[str, Any]) -> dict[str, Any]:
    d = dict(payload_dict)  # shallow copy

    cols = d.get("columns") or []
    d["columns_count"] = len(cols)
    d["columns_sample"] = cols[:10]
    d.pop("columns", None)

    return d


def awards_usas_to_sql(year, month, no_months, period_months=12):
    def get_status(status_url):
        logger.info(f"GET status: {status_url}")
        resp = requests.get(status_url, headers=USER_AGENT, timeout=60)
        resp.raise_for_status()
        j = resp.json()
        logger.info(f"status response: {j}")
        return j["status"]

    payloads = get_awards_payloads(year, month, no_months, period_months)
    logger.info("Starting seed run")
    logger.info(f"payload count: {len(payloads)}")
    logger.info(
        f"payload filter date ranges: {[p.filters.date_range for p in payloads]}"
    )

    conn = engine.raw_connection()
    cursor = conn.cursor()
    logger.info("DB connection established; starting downloads")

    for payload in payloads:
        payload_dict = payload.dict()

        logger.info(
            "POST %s headers=%s body=%s",
            AWARDS_DL_EP,
            _sanitize_headers(USER_AGENT),
            json.dumps(_payload_for_log(payload_dict), sort_keys=True),
        )

        t0 = time.monotonic()
        r = requests.post(
            AWARDS_DL_EP, json=payload_dict, headers=USER_AGENT, timeout=60
        )
        dt = time.monotonic() - t0

        logger.info(
            "POST response status=%s elapsed=%.3fs content_type=%s",
            r.status_code,
            dt,
            r.headers.get("content-type"),
        )

        if not r.ok:
            logger.error("POST error body=%s", r.text[:2000])
            r.raise_for_status()

        j = r.json()
        logger.info("POST json keys=%s", sorted(j.keys()))

        logger.info(f"date_range: {payload.filters.date_range}")
        logger.info(f"file_url: {j.get('file_url')}")
        logger.info(f"status_url: {j.get('status_url')}")

        status_url = j["status_url"]
        file_url = j["file_url"]

        status = get_status(status_url)
        logger.info("Entering poll loop")

        while status not in ("failed", "finished"):
            logger.info(f"status={status}; sleeping 30s")
            sleep(30)
            status = get_status(status_url)

        if status == "failed":
            raise RuntimeError("download failed")

        logger.info(f"Downloading zip: {file_url}")
        file = requests.get(file_url, stream=True, timeout=300)
        file.raise_for_status()

        with tempfile.TemporaryDirectory() as raw_data:
            logger.info(f"tempdir: {raw_data}")
            with ZipFile(BytesIO(file.content), "r") as zip_ref:
                zip_ref.extractall(raw_data)

            files = glob("*.csv", root_dir=raw_data)
            logger.info(f"csv files: {files}")

            for csv_name in files:
                copy_cmd = generate_copy_from_sql(csv_name)
                logger.info(f"copy_cmd for {csv_name}: {copy_cmd}")

                with open(f"{raw_data}/{csv_name}", "r") as f:
                    cursor.copy_expert(copy_cmd, f)
                    conn.commit()
                    logger.info(f"committed {csv_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download all prime award transaction data from USAspending within specified date range"
    )
    parser.add_argument(
        "-s",
        metavar="start_date",
        type=str,
        help="YYYY-MM-DD Filter transactions by action_date >= (required).",
        required=True,
    )
    parser.add_argument(
        "-e",
        metavar="end_date",
        type=str,
        help="YYYY-MM-DD Filter transactions by action_date <= (default = today).",
        required=False,
    )
    args = parser.parse_args()
    awards_usas_to_sql(args.s, args.e)

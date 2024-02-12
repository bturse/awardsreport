import argparse
import requests
from time import sleep
from zipfile import ZipFile
from io import BytesIO
from glob import glob
from typing import Optional
import tempfile

import logging.config
from awardsreport import log_config

logging.config.dictConfig(log_config.LOGGING_CONFIG)
logger = logging.getLogger("awardsreport")


from awardsreport.database import engine, Base
from awardsreport.models import ProcurementTransactions, AssistanceTransactions
from awardsreport.setup.seed_helpers import (
    get_awards_payloads,
    generate_copy_from_sql,
    USER_AGENT,
    AWARDS_DL_EP,
)


# this function could be optimized by initiating all downloads at once.
def awards_usas_to_sql(start_date: str, end_date: Optional[str] = None):
    """Download all awards data in date range from USAspending to sql.

    args
        start_date: Earliest date in range format as YYYY-MM-DD.
        end_date: Last date in range format as YYYY-MM-DD.

    return None
    """

    def get_status(status_url):
        return requests.get(status_url, headers=USER_AGENT).json()["status"]

    payloads = get_awards_payloads(start_date, end_date)
    logger.info(
        f"payload filter date ranges: {[payload.filters.date_range for payload in payloads]}"
    )

    conn = engine.raw_connection()
    cursor = conn.cursor()
    logger.info(f"conn: {conn}")
    logger.info(f"cursor: {conn}")

    status_file_urls = []

    for payload in payloads:
        logger.info(AWARDS_DL_EP)
        logger.info(payload.dict())
        r = requests.post(AWARDS_DL_EP, json=payload.dict(), headers=USER_AGENT).json()
        logger.info(f"date_range: [{payload.filters.date_range}]")
        logger.info(f"file_url: {r['file_url']}")
        logger.info(f"status_url: {r['status_url']}")
        status_file_urls.append((r["status_url"], r["file_url"]))
        sleep(60)

    logger.info(f"status_file_urls: {status_file_urls}")

    for status_url, file_url in status_file_urls:
        status = get_status(status_url)
        logger.info(status_url)
        logger.info(f"status: {status}")
        logger.info("entering request rest loop")
        while status not in ("failed", "finished"):
            sleep(300)
            status = get_status(status_url)

        if status == "failed":
            logger.error("status == 'failed' raising Exception('download failed')")
            raise Exception("download failed")
        if status == "finished":
            logger.info(f"status: {status}")
            logger.info(f"requesting: {file_url}")
            try:
                file = requests.get(file_url, stream=True)
                with tempfile.TemporaryDirectory() as temp_dir:
                    with tempfile.TemporaryFile(temp_dir) as temp_file:
                        logger.info(f"temp_file: {temp_file}")
                        for chunk in file.iter_content(512):
                            temp_file.write(chunk)
                        with ZipFile(temp_file, "r") as zip_ref:
                            files = glob("*.csv", root_dir=temp_dir)
                            logger.info(f"files: {files}")
                            zip_ref.extractall(temp_dir)
                        for file in files:
                            logger.info(f"file: {file}")
                            copy_cmd = generate_copy_from_sql(file)
                            logger.info(f"copy_cmd: {copy_cmd}")
                            cursor.copy_expert(copy_cmd, temp_file)
                            conn.commit()
                            logger.info("commit completed")
            except Exception:
                raise Exception(f"Unable to import {file_url}")


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

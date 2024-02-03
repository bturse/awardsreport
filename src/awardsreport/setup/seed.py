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
    """Download all awards data in range from USAspending to sql.

    args
        year int the last year of the date range.
        month int the last month of the date range.
        no_months int the number of months prior to the specified month.

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

    for payload in payloads:
        r = requests.post(AWARDS_DL_EP, json=payload.dict(), headers=USER_AGENT).json()
        logger.info(f"date_range: [{payload.filters.date_range}]")
        logger.info(f"file_url: {r['file_url']}")
        logger.info(f"status_url: {r['status_url']}")
        status = get_status(r["status_url"])
        logger.info(f"status: {status}")
        logger.info("entering request rest loop")
        while status not in ("failed", "finished"):
            sleep(300)
            status = get_status(r["status_url"])

        if status == "failed":
            logger.error("status == 'failed' raising Exception('download failed')")
            raise Exception("download failed")
        if status == "finished":
            logger.info(f"status: {status}")
            logger.info(f"requesting: {r['file_url']}")
            try:
                file = requests.get(r["file_url"], stream=True)
                with tempfile.TemporaryDirectory() as raw_data:
                    logger.info(f"temp: {raw_data}")
                    with ZipFile(BytesIO(file.content), "r") as zip_ref:
                        logger.info("extracting zip data")
                        zip_ref.extractall(raw_data)
                        files = glob("*.csv", root_dir=raw_data)
                        logger.info(f"files: {files}")
                        for file in files:
                            logger.info(f"file: {file}")
                            copy_cmd = generate_copy_from_sql(file)

                            logger.info(f"copy_cmd: {copy_cmd}")
                            with open(f"{raw_data}/{file}", "r") as f:
                                cursor.copy_expert(copy_cmd, f)
                                conn.commit()
                                logger.info("commit completed")
            except Exception:
                raise Exception(f"Unable to import {r['file_url']}")


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

import argparse
import os
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


# https://github.com/python/cpython/pull/29560
class SpooledTemporaryFile(tempfile.SpooledTemporaryFile):
    def seekable(self) -> bool:
        return super()._file.seekable()


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
        r = requests.post(AWARDS_DL_EP, json=payload.dict(), headers=USER_AGENT)
        r.raise_for_status()
        r = r.json()
        logger.info(f"date_range: [{payload.filters.date_range}]")
        logger.info(f"file_url: {r['file_url']}")
        logger.info(f"status_url: {r['status_url']}")
        status_file_urls.append((r["status_url"], r["file_url"]))
        sleep(30)

    logger.info(f"status_file_urls: {status_file_urls}")

    for status_url, file_url in status_file_urls:
        status = get_status(status_url)
        logger.info(status_url)
        logger.info(f"status: {status}")
        logger.info("entering request rest loop")
        while status not in ("failed", "finished"):
            sleep(30)
            status = get_status(status_url)

        if status == "failed":
            logger.error("status == 'failed' raising Exception('download failed')")
            raise Exception("download failed")

        if status == "finished":
            logger.info(f"requesting: {file_url}")
            try:
                response = requests.get(file_url, stream=True)
                logger.info(response)
                logger.info(f"file headers: {response.headers}")
                response.raise_for_status()

                try:
                    total_size = int(response.headers["Content-Length"])
                except ValueError as e:
                    raise e

                logger.info(f"total file size: {total_size}")
                with tempfile.TemporaryDirectory() as temp_dir:
                    with SpooledTemporaryFile(
                        max_size=1024 * 1024 * 100, dir=temp_dir
                    ) as temp_file:
                        logger.info(f"temporary file created: {temp_file}")
                        # chunk_size should be removed if response.iter_content(chunk_size=None)
                        # also, remove from progress loader.
                        chunk_size = 1024 * 64
                        downloaded_size = 0

                        for chunk in response.iter_content(chunk_size=chunk_size):
                            temp_file.write(chunk)
                            downloaded_size += len(chunk)

                            if total_size > 0:
                                progress = (downloaded_size / total_size) * 100
                                if progress % 10 < (chunk_size / total_size) * 100:
                                    logger.info(f"download progress: {progress:.2f}%")
                        logger.info(
                            f"Downloaded {downloaded_size} of {total_size} bytes"
                        )
                        if downloaded_size < total_size:
                            raise Exception(
                                f"Downloaded file size {downloaded_size} is less than expected {total_size}"
                            )

                        logger.info(f"flushing temp file: {temp_file}")
                        temp_file.flush()
                        logger.info(f"flush complete")
                        logger.info(f"seek(0) temp file: {temp_file}")
                        temp_file.seek(0)
                        logger.info(f"seek complete")
                        try:
                            with ZipFile(temp_file, "r") as zip_ref:
                                logger.info(
                                    f"ZIP file content names: {zip_ref.namelist()}"
                                )
                                zip_ref.extractall(temp_dir)
                                logger.info(f"extracted ZIP file to: {temp_dir}")
                                csv_files = glob(f"{temp_dir}/*.csv", root_dir=temp_dir)
                                logger.info(f"begin processing csv files")
                                for csv_file in csv_files:
                                    logger.info(f"Processing file: {csv_file}")
                                    with open(csv_file, "r", encoding="utf-8") as f:
                                        copy_cmd = generate_copy_from_sql(csv_file)
                                        logger.info(
                                            f"generated COPY command: {copy_cmd}"
                                        )
                                        cursor.copy_expert(copy_cmd, f)
                                    logger.info(
                                        f"processing complete for file: {csv_file}"
                                    )
                                    logger.info(f"committing file: {csv_file}")
                                    conn.commit()
                                    logger.info(f"commit complete for file: {csv_file}")
                        except Exception as e:
                            logger.error(e)
                            raise e
            except Exception as e:
                logger.error(e)
                conn.rollback()
                raise


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

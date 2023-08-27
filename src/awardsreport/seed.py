import requests
from time import sleep
from zipfile import ZipFile
from io import BytesIO, StringIO
from glob import glob
import tempfile
import logging

from awardsreport.database import engine, Base
from awardsreport.models import ProcurementTransactions, AssistanceTransactions
from awardsreport.seed_helpers import (
    get_awards_payloads,
    generate_copy_from_sql,
    YEAR,
    MONTH,
    USER_AGENT,
    AWARDS_DL_EP,
)

logging.basicConfig(
    filename=f"{__name__}.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d  %(message)s",
)


# this function could be optimized by initiating all downloads at once.
def awards_usas_to_sql(year, month, no_months, period_months=12):
    """Download all awards data in range from USAspending to sql.

    args
        year int the last year of the date range.
        month int the last month of the date range.
        no_months int the number of months prior to the specified month.

    return None
    """

    def get_status(status_url):
        return requests.get(status_url, headers=USER_AGENT).json()["status"]

    payloads = get_awards_payloads(year, month, no_months, period_months)
    logging.info(
        f"payload filter date ranges: {[payload['filters']['date_range'] for payload in payloads]}"
    )

    conn = engine.raw_connection()
    cursor = conn.cursor()
    logging.info(f"conn: {conn}")
    logging.info(f"cursor: {conn}")

    for payload in payloads:
        r = requests.post(AWARDS_DL_EP, json=payload, headers=USER_AGENT).json()
        logging.info(f"date_range: [{payload['filters']['date_range']}]")
        logging.info(f"file_url: {r['file_url']}")
        logging.info(f"status_url: {r['status_url']}")
        status = get_status(r["status_url"])
        logging.info(f"status: {status}")
        logging.info("entering request rest loop")
        while status not in ("failed", "finished"):
            sleep(300)
            status = get_status(r["status_url"])

        if status == "failed":
            logging.error("status == 'failed' raising Exception('download failed')")
            raise Exception("download failed")
        if status == "finished":
            logging.info(f"status: {status}")
            logging.info(f"requesting: {r['file_url']}")
            try:
                file = requests.get(r["file_url"], stream=True)
                with tempfile.TemporaryDirectory() as raw_data:
                    logging.info(f"temp: {raw_data}")
                    with ZipFile(BytesIO(file.content), "r") as zip_ref:
                        logging.info("extracting zip data")
                        zip_ref.extractall(raw_data)
                        files = glob("*.csv", root_dir=raw_data)
                        logging.info(f"files: {files}")
                        for file in files:
                            logging.info(f"file: {file}")
                            copy_cmd = generate_copy_from_sql(file)

                            logging.info(f"copy_cmd: {copy_cmd}")
                            with open(f"{raw_data}/{file}", "r") as f:
                                cursor.copy_expert(copy_cmd, f)
                                conn.commit()
                                logging.info("commit completed")
            except Exception:
                raise Exception(f"Unable to import {r['file_url']}")


if __name__ == "__main__":
    awards_usas_to_sql(YEAR, MONTH, 1, 1)

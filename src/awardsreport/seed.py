import requests
from time import sleep
from zipfile import ZipFile
from io import BytesIO, StringIO
from glob import glob
import tempfile
import logging

from awardsreport.database import engine, Base
from awardsreport.models import Transactions, AssistanceTransactions
from awardsreport.helpers.seed_helpers import (
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
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


# this function could be optimized by initiating all downloads at once.
def awards_usas_to_sql(year, month, no_months):
    """Download all awards data in range from USAspending to sql.

    args
        year int the last year of the date range.
        month int the last month of the date range.
        no_months int the number of months prior to the specified month.

    return None
    """
    logging.info("entering awards_24_mo_usas_to_sql")

    payloads = get_awards_payloads(year, month, no_months)
    logging.info("set up ep and payloads")

    conn = engine.raw_connection()
    cursor = conn.cursor()
    logging.info("set up conn and cursor")
    logging.info(conn)
    logging.info(cursor)

    for payload in payloads:
        logging.info("processing payloads")
        r = requests.post(AWARDS_DL_EP, json=payload, headers=USER_AGENT).json()[
            "status_url"
        ]
        logging.info(r.text)
        logging.info("payload response:")
        logging.info(r)
        status_url = r["status_url"]
        status = requests.get(status_url, headers=USER_AGENT).json()["status"]
        logging.info(f"status: {status}")
        logging.info("beginning status check while loop")
        while status not in ("failed", "finished"):
            logging.info(f"starting status: {status}")
            sleep(120)
            status = requests.get(status_url, headers=USER_AGENT).json()["status"]
            logging.info(f"ending status: {status}")
        logging.info("breaking from status check while loop")

        if status == "failed":
            logging.error("status == 'failed' raising Exception('download failed')")
            raise Exception("download failed")
        if status == "finished":
            logging.info("status == 'finished'")
            logging.info(f"requesting file: {r['file_url']}")
            file = requests.get(r["file_url"], stream=True)
            logging.info(f"file url: {file}")

        with tempfile.TemporaryDirectory() as raw_data:
            logging.info("creating TemporaryDirectory")
            logging.info(raw_data)
            with ZipFile(StringIO(file.content), "r") as zip_ref:
                logging.info("extracting zip data")
                zip_ref.extractall(raw_data)
                files = glob("*.csv", root_dir=raw_data)
                logging.info("processing files")
                logging.info(files)
                for file in files:
                    logging.info(f"processing file: {file}")
                    if "Assistance" in file:
                        logging.info("assistance file")
                        cmd = generate_copy_from_sql("assistance")
                    if "Contract" in file:
                        logging.info("contract file")
                        cmd = generate_copy_from_sql("procurement")

                    logging.info(f"command: {cmd}")
                    path = f"{raw_data}/{file}"
                    logging.info(f"file path: {path}")
                    with open(path, "r") as f:
                        logging.info(f"opening file: {path}")
                        logging.info("running copy_expert")
                        cursor.copy_expert(cmd, f)
                        logging.info("copy_expert completed")
                        conn.commit()
                        logging.info("commit completed")


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    logging.info("dropped metadata")
    Base.metadata.create_all(engine)
    logging.info("created metadata")
    awards_usas_to_sql(YEAR, MONTH - 1, 13)

import uvicorn
from fastapi import FastAPI
from awardsreport.routers import topline, summary_tables
from dotenv import load_dotenv
import os
from awardsreport.database import Session

import logging.config
from awardsreport import log_config

logging.config.dictConfig(log_config.LOGGING_CONFIG)
logger = logging.getLogger("awardsreport")

load_dotenv()


app = FastAPI()
app.include_router(summary_tables.router)
app.include_router(topline.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.environ["DB_HOST"],
        reload=True,
        log_level="info",
    )

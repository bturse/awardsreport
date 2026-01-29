import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from awardsreport.routers import summary_tables
from awardsreport.logging_setup import setup_logging

load_dotenv()

setup_logging()

app = FastAPI()
app.include_router(summary_tables.router)

if __name__ == "__main__":
    uvicorn.run(
        "awardsreport.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

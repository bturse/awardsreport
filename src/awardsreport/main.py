import uvicorn
from fastapi import FastAPI
from awardsreport.routers import topline
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()
app.include_router(topline.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.environ["DB_HOST"],
        #        log_config="../../log.ini",
    )

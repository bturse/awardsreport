from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base

# from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()


Base = declarative_base()

url_object = URL.create(
    drivername=os.environ["DB_DRIVER"],
    username=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=os.environ["DB_PORT"],
    database=os.environ["DB_DATABASE"],
)

engine = create_engine(url_object)
Session = sessionmaker(bind=engine)

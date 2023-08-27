from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
import os
from dotenv import load_dotenv
from typing import Generator

load_dotenv()


class Base(DeclarativeBase):
    pass


url_object: URL = URL.create(
    drivername=os.environ["DB_DRIVER"],
    username=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_DATABASE"],
)

engine = create_engine(url_object, echo=True)
sess = sessionmaker(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db: Session = sess()
    try:
        yield db
    finally:
        db.close()

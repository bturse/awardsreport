import pytest

from awardsreport.database import Base, engine, Session


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)

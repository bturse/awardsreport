import pytest
from alembic import command
from alembic.config import Config
from awardsreport.database import Base, engine, Session, url_object


@pytest.fixture(scope="function")
def alembic_config():
    config = Config("alembic.ini")
    return config


@pytest.fixture(scope="function")
def setup_database(alembic_config):
    command.upgrade(alembic_config, "head")
    yield


@pytest.fixture(autouse=True)
def db_session(setup_database):
    pass

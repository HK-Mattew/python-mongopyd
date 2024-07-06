import pytest
import pymongo

from config import (
    MONGO_DB_URI,
    MONGO_DB_NAME
    )

from mongopyd import configure_databases
from mongopyd.database import DataBase


client = pymongo.MongoClient(MONGO_DB_URI)
database = client[MONGO_DB_NAME]

configure_databases([
    DataBase(
        alias='default',
        db=database,
        is_default=True
    )
])


@pytest.fixture()
def pymongo_database():
    
    return database



import pytest
import pymongo
import motor.motor_asyncio

from config import (
    MONGO_DB_URI,
    MONGO_DB_NAME
    )

from mongopyd import configure_databases
from mongopyd.database import DataBase, AsyncDataBase


client = pymongo.MongoClient(MONGO_DB_URI)
database = client[MONGO_DB_NAME]

motor_client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_DB_URI
)
motor_db = motor_client[MONGO_DB_NAME]

configure_databases([
    DataBase(
        alias='default',
        db=database,
        is_default=True
    ),
    AsyncDataBase(
        alias='default',
        db=motor_db,
        is_default=True
    )
])


@pytest.fixture()
def pymongo_database():
    
    return database

@pytest.fixture()
def motor_database():
    
    return motor_db



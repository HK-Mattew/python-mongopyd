from dataclasses import dataclass
import motor.motor_asyncio
import pymongo



@dataclass
class DataBase:
    alias: str
    db: pymongo.database.Database
    is_default: bool = False


    def __post_init__(self):

        if not isinstance(self.db, pymongo.database.Database):
            raise ValueError('The db parameter must be an instance of: `pymongo.database.Database`')
        



@dataclass
class AsyncDataBase:
    alias: str
    db: motor.motor_asyncio.AsyncIOMotorDatabase
    is_default: bool = False


    def __post_init__(self):

        if not isinstance(self.db, motor.motor_asyncio.AsyncIOMotorDatabase):
            raise ValueError('The db parameter must be an instance of: `motor.motor_asyncio.AsyncIOMotorDatabase`')




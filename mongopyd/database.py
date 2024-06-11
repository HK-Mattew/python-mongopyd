from dataclasses import dataclass
from typing import (
    Union
)
import motor.motor_asyncio
import pymongo



@dataclass
class DataBase:
    db: Union[pymongo.database.Database, motor.motor_asyncio.AsyncIOMotorDatabase]
    is_default: bool = False




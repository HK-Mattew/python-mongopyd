from .database import DataBase
from typing import (
    Dict,
    List
    )



DATABASES: Dict[str, DataBase] = {}

DEFAULT_DATABASE = None





def configure_databases(
        databases: List[DataBase]
    ) -> Dict[str, DataBase]:


    if len(DATABASES) > 0:
        raise RuntimeError('Database configuration can only be done once')


    if not isinstance(databases, list):
        raise ValueError(f'DataBases must be a list of `{DataBase}`')

    if not databases:
        raise ValueError('DataBase list is empty')


    _DEFAULT_DATABASE = None

    for database in databases:

        if not isinstance(database, DataBase):
            raise ValueError(f'The database list must contain only {DataBase} objects')


        DATABASES[database.db.name] = database

        if database.is_default and _DEFAULT_DATABASE is not None:
            raise ValueError('Only one database can be set as default')
        
        if database.is_default:
            _DEFAULT_DATABASE = database


    if _DEFAULT_DATABASE is None:
        raise ValueError('At least one database must be defined as default')


    global DEFAULT_DATABASE
    DEFAULT_DATABASE = _DEFAULT_DATABASE

    return get_databases()



def get_database(name: str = None) -> DataBase:

    if name is not None:
        return DATABASES[name]
    else:
        return DEFAULT_DATABASE



def get_databases() -> Dict[str, DataBase]:
    return DATABASES



from .async_document import Document as AsyncDocument
from .sync_document import Document

from .database import DataBase
from typing import (
    Dict,
    List
    )



DATABASES: Dict[str, DataBase] = {}

DEFAULT_DATABASE_ALIAS = None





def configure_databases(
        databases: List[DataBase]
    ) -> Dict[str, DataBase]:


    if len(DATABASES) > 0:
        raise RuntimeError('Database configuration can only be done once')


    if not isinstance(databases, list):
        raise ValueError(f'DataBases must be a list of `{DataBase}`')

    if not databases:
        raise ValueError('DataBase list is empty')


    _DEFAULT_DATABASE_ALIAS = None

    for database in databases:

        if not isinstance(database, DataBase):
            raise ValueError(f'The database list must contain only {DataBase} objects')


        if get_database(alias=database.alias):
            raise ValueError('Database aliases must be unique')


        DATABASES[database.alias] = database

        if database.is_default and _DEFAULT_DATABASE_ALIAS is not None:
            raise ValueError('Only one database can be set as default')
        
        if database.is_default:
            _DEFAULT_DATABASE_ALIAS = database.alias


    if _DEFAULT_DATABASE_ALIAS is None:
        raise ValueError('At least one database must be defined as default')


    global DEFAULT_DATABASE_ALIAS
    DEFAULT_DATABASE_ALIAS = _DEFAULT_DATABASE_ALIAS

    return get_databases()



def get_database(alias: str = None) -> DataBase:

    if alias is not None:
        return DATABASES[alias]
    else:
        return DATABASES[DEFAULT_DATABASE_ALIAS]



def get_databases() -> Dict[str, DataBase]:
    return DATABASES



from .async_document import Document as AsyncDocument
from .sync_document import Document

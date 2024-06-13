from .database import DataBase, AsyncDataBase
from typing import (
    Optional,
    Literal,
    Union,
    Dict,
    List
    )



DATABASES: Dict[str, DataBase] = {}
ASYNC_DATABASES: Dict[str, AsyncDataBase] = {}

DEFAULT_DATABASE_ALIAS = None
ASYNC_DEFAULT_DATABASE_ALIAS = None




def configure_databases(
        databases: List[Union[DataBase, AsyncDataBase]]
    ) -> Dict[Literal['sync', 'async'], Dict[str, Union[DataBase, AsyncDataBase]]]:


    if len(DATABASES) > 0 or len(ASYNC_DATABASES) > 0:
        raise RuntimeError('Database configuration can only be done once')


    if not isinstance(databases, list):
        raise ValueError(f'DataBases must be a list of `{DataBase}` or `{AsyncDataBase}`')


    if not databases:
        raise ValueError('DataBases list is empty')


    _DEFAULT_DATABASE_ALIAS = None
    _ASYNC_DEFAULT_DATABASE_ALIAS = None


    for database in databases:

        if not isinstance(database, DataBase) and not isinstance(database, AsyncDataBase):
            raise ValueError(f'The database list must contain only {DataBase} or {AsyncDataBase} objects')


        if isinstance(database, DataBase):
            database_mode = 'sync'
        else:
            database_mode = 'async'


        if get_database(mode=database_mode, alias=database.alias):
            raise ValueError(
                'Database aliases must be unique between modes (DataBase and AsyncDatabase).'
                )


        if database_mode == 'sync':
            DATABASES[database.alias] = database

            if database.is_default and _DEFAULT_DATABASE_ALIAS is not None:
                raise ValueError(
                    'Only one database can be set as default per mode (DataBase and AsyncDataBase).'
                    )
            
            if database.is_default:
                _DEFAULT_DATABASE_ALIAS = database.alias
            
        else:
            ASYNC_DATABASES[database.alias] = database

            if database.is_default and _ASYNC_DEFAULT_DATABASE_ALIAS is not None:
                raise ValueError(
                    'Only one database can be set as default per mode (DataBase and AsyncDataBase).'
                    )
            
            if database.is_default:
                _ASYNC_DEFAULT_DATABASE_ALIAS = database.alias


    global DEFAULT_DATABASE_ALIAS
    DEFAULT_DATABASE_ALIAS = _DEFAULT_DATABASE_ALIAS

    global ASYNC_DEFAULT_DATABASE_ALIAS
    ASYNC_DEFAULT_DATABASE_ALIAS = _ASYNC_DEFAULT_DATABASE_ALIAS


    _RETURN_DATABASES = {
        'sync': get_databases(mode='sync'),
        'async': get_databases(mode='async')
    }

    return _RETURN_DATABASES




def get_database(mode: Literal['sync', 'async'], alias: str = None) -> Optional[Union[DataBase, AsyncDataBase]]:

    mode = mode.lower()

    if mode == 'sync':

        if alias is not None:
            return DATABASES.get(alias, None)
        else:

            if DEFAULT_DATABASE_ALIAS is None:
                raise RuntimeError('No default database has been set for `sync` mode.')

            return DATABASES.get(DEFAULT_DATABASE_ALIAS, None)
        
    else:

        if alias is not None:
            return ASYNC_DATABASES.get(alias, None)
        else:

            if ASYNC_DEFAULT_DATABASE_ALIAS is None:
                raise RuntimeError('No default database has been set for `async` mode.')

            return ASYNC_DATABASES.get(ASYNC_DEFAULT_DATABASE_ALIAS, None)



def get_databases(mode: Literal['sync', 'async']) -> Dict[str, Optional[Union[DataBase, AsyncDataBase]]]:

    mode = mode.lower()

    if mode == 'sync':
        return DATABASES.copy()

    elif mode == 'async':
        return ASYNC_DATABASES.copy()
    
    else:
        raise ValueError(f'Mode `{mode}` is invalid.')
    


from .async_document import AsyncDocument
from .sync_document import Document

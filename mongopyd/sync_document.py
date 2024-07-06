from pydantic import (
    BaseModel,
    Field
)
from typing import (
    List,
    Dict,
    Any,
    Mapping,
    Union,
    Sequence,
    Optional
)
import pymongo
from pymongo import (
    ReturnDocument
)
from bson import ObjectId
from pymongo.errors import (
    DuplicateKeyError
)
import functools


from . import get_database
from .src.custom_types import PydanticObjectId



def need_database_and_collection(func):

    @functools.wraps(func)
    def wrapper(
        self,
        *args,
        database: Optional[Union[str, pymongo.database.Database]] = None,
        collection: Optional[Union[str, pymongo.collection.Collection]] = None,
        **kwargs):


        if database is None or isinstance(database, str):

            if database is not None:
                
                _database = get_database(
                    mode='sync',
                    alias=database
                )

                if _database is None:
                    raise RuntimeError(
                        f'No database was found for the alias `{database}` and no default database was found either.'
                        )
                else:
                    database = _database.db

            else:

                try:
                    db_alias = self.Settings.db_alias
                except AttributeError:
                    """
                    It will get the default database configured in the method: configure database(...)
                    """
                    db_alias = None

                _database = get_database(
                    mode='sync',
                    alias=db_alias
                )

                if _database is None:
                    raise RuntimeError(
                        f'No database was found for the alias `{db_alias}` and no default database was found either.'
                        )
                else:
                    database = _database.db


        if not isinstance(database, pymongo.database.Database):
            raise RuntimeError(
                f"Database instance `{database.__class__}` is invalid." \
                     f" It must be an instance of: `<class 'pymongo.database.Database'>`"
                )


        if collection is None or isinstance(collection, str):

            if collection is not None:

                collection = database.get_collection(
                    collection
                    )
            else:

                try:
                    coll_name = self.Settings.name
                except AttributeError:
                    raise AttributeError(f'The Settings.name must be specified in the model.')
                
                if coll_name is None:
                    raise ValueError('The Settings.name must be specified in the model.')

                collection = database.get_collection(
                    coll_name
                    )


        if not isinstance(collection, pymongo.collection.Collection):
            raise RuntimeError(
                f"Collection instance `{collection.__class__}` is invalid." \
                     f" It must be an instance of: `<class 'pymongo.collection.Collection'>`"
                )


        return func(self,
            *args,
            database=database,
            collection=collection,
            **kwargs)


    return wrapper



class Document(BaseModel):

    id: Optional[PydanticObjectId] = Field(default=None, alias='_id')


    # Pydantic configs: https://docs.pydantic.dev/latest/usage/model_config/#options
    class Config():
        extra = 'allow'
        json_encoders = {
            PydanticObjectId: lambda v: str(v),
        }
        arbitrary_types_allowed = True

    class Settings():
        name = None
        db_alias = None
        indexes = []



    @classmethod
    @need_database_and_collection
    def build_indexes(
        self,
        database: Optional[Union[str, pymongo.database.Database]] = None,
        collection: Optional[Union[str, pymongo.collection.Collection]] = None
        ):

        try:
            getattr(self, 'Settings')
        except AttributeError:
            return None
    

        try:
            indexes = getattr(self.Settings, 'indexes')
            if not indexes:
                return None
        except AttributeError:
            return None
        

        return  collection.create_indexes(indexes)


    @classmethod
    @need_database_and_collection
    def find(
        self,
        filter: Mapping[str, Any],
        database: Optional[Union[str, pymongo.database.Database]] = None,
        collection: Optional[Union[str, pymongo.collection.Collection]] = None,
        **kwargs: Any
        ):
        

        results = collection.find(filter, **kwargs)
        for result in results:
            ins_result = self(**result)
            yield ins_result


    @classmethod
    @need_database_and_collection
    def find_one(
        self,
        filter: Union[Dict[str, Any], ObjectId, str],
        update: Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]=None,
        database: Optional[Union[str, pymongo.database.Database]] = None,
        collection: Optional[Union[str, pymongo.collection.Collection]] = None,
        **kwargs: Any
        ):


        if 'return_document' in kwargs:
            raise ValueError('You cannot use return_document as a parameter')


        if isinstance(filter, ObjectId):
            filter = {'_id': filter}

        elif isinstance(filter, str):
            filter = {'_id': ObjectId(filter)}


        if not update:
            result =  collection.find_one(filter, **kwargs)
        else:
            result =  collection.find_one_and_update(
                filter=filter,
                update=update,
                return_document=ReturnDocument.AFTER,
                **kwargs)
        
        
        if result is None:
            return None

        return self(**result)
    

    @need_database_and_collection
    def update(self,
        filter: Mapping[str, Any],
        update: Union[Mapping[str, Any], Sequence[Mapping[str, Any]]],
        database: Optional[Union[str, pymongo.database.Database]] = None,
        collection: Optional[Union[str, pymongo.collection.Collection]] = None,
        **kwargs: Any
        ):

        try:
            if self.id is None:
                raise RuntimeError('You must fetch a document first')
        except AttributeError:
            raise RuntimeError('You must fetch a document first')


        if '_id' in filter: del filter['_id']

        base_filter = {
            '_id': self.id,
            **filter
        }

        if 'return_document' in kwargs:
            raise ValueError('You cannot use return_document as a parameter')

        result =  collection.find_one_and_update(
                filter=base_filter,
                update=update,
                return_document=ReturnDocument.AFTER,
                **kwargs)

        if not result:
            """
            Document not found. Not even a document corresponds to query of consultation.
            """
            return False
        
        self.reload_with_dict(result)

        return True


    @need_database_and_collection
    def update_with_custom_queryes(
        self,
        queryes: list,
        database: Optional[Union[str, pymongo.database.Database]] = None,
        collection: Optional[Union[str, pymongo.collection.Collection]] = None,
        **kwargs
        ):

        query_update = {}
        # fields_reload = []

        for custom_query in queryes:
            for operator, data in custom_query.items():
                if not operator.startswith('$'):
                    raise ValueError('The custom query key must start with $')

                if data and not operator in query_update:
                    query_update[operator] = {}

                for field_name, field_value in data.items():
                    query_update[operator][field_name] = field_value
                    # fields_reload.append(field_name)
                
        
        match_query = query_update.get('$match', {})
        if '$match' in query_update: del query_update['$match']

        return  self.update(
            filter=match_query,
            update=query_update,
            database=database,
            collection=collection,
            **kwargs
            )


    @need_database_and_collection
    def insert(
        self,
        allow_nulls: bool= False,
        database: Optional[Union[str, pymongo.database.Database]] = None,
        collection: Optional[Union[str, pymongo.collection.Collection]] = None,
        **kwargs
        ):

        if allow_nulls:
            doc_data = self.model_dump(by_alias=True)
        else:
            doc_data = self.model_dump(
                by_alias=True,
                exclude_none=True
            )


        if '_id' in doc_data and doc_data['_id'] is None:
            del doc_data['_id']


        try:
            result = collection.insert_one(
                doc_data,
                **kwargs
            )
        except DuplicateKeyError as err:
            raise DuplicateKeyError(
                'This document is already inserted or another document has the same id' \
                f' | Server error: {err._message}'
            )

        self.reload_with_dict({'_id': result.inserted_id})

        return result.inserted_id


    @need_database_and_collection
    def delete(
        self,
        filter: Union[Dict[str, Any], ObjectId, str],
        database: Optional[Union[str, pymongo.database.Database]] = None,
        collection: Optional[Union[str, pymongo.collection.Collection]] = None,
        **kwargs):
        
        try:
            if self.id is None:
                raise RuntimeError('You must fetch a document first')
        except AttributeError:
            raise RuntimeError('You must fetch a document first')


        if '_id' in filter: del filter['_id']

        base_filter = {
            '_id': self.id,
            **filter
        }

        result =  collection.find_one_and_delete(
            filter=base_filter,
            **kwargs)

        if not result:
            """
            Document not found. Not even a document corresponds to query of consultation.
            """
            return False
        
        self.reload_with_dict(result)
        return True


    @classmethod
    @need_database_and_collection
    def count_documents(
        self,
        filter: Mapping[str, Any],
        database: Optional[Union[str, pymongo.database.Database]] = None,
        collection: Optional[Union[str, pymongo.collection.Collection]] = None,
        **kwargs: Any
        ) -> int:

        return collection.count_documents(filter, **kwargs) 


    @need_database_and_collection
    def reload(
        self,
        fields: List[str]=[],
        database: Optional[Union[str, pymongo.database.Database]] = None,
        collection: Optional[Union[str, pymongo.collection.Collection]] = None,
        **kwargs
        ):

        
        base_filter = {
            '_id': self.id
        }

        if isinstance(fields, list) and fields:

            if list(filter(lambda x: '.' in x, fields)):
                raise ValueError('It is not possible to use dot annotation on reload.')

            result =  collection.find_one(
                base_filter,
                projection=fields,
                **kwargs
                )
        else:
            result =  collection.find_one(base_filter, **kwargs)
        
        if not result:
            return Exception('This document does not exist')


        self.reload_with_dict(result)
        return True

        
    def get(self, field: Any, default: Any=None):
        """
        #Grab data in the document in the following ways:
        
        # 1 - get field
        self.get('field_name')

        # 2 - To get the value of a field within a dictionary within the document
        self.get('field_name.field_name2')
        
        """

        if field == 'id':
            return self.get('_id', default=default)


        document = self.model_dump(by_alias=True)
        value = None
        _refs = field.split('.')

        for _ref in _refs:
            if value is None:
                if _ref != _refs[-1]:
                    value = document.get(_ref, {})
                else:
                    value = document.get(_ref, default)
            else:
                if _ref != _refs[-1]:
                    if isinstance(value, dict):
                        value = value.get(_ref, {})
                    else:
                        raise ValueError('The value you are trying to get is not a dictionary')
                else:
                    if isinstance(value, dict):
                        value = value.get(_ref, default)
                    else:
                        raise ValueError(f'The value you are trying to get is not a dictionary')


        return value


    def reload_with_dict(self, data: Dict[str, Any]):
        for key, value in data.items():
            if key == '_id':
                key = 'id'

            try:
                self.__setattr__(key, value)
            except AttributeError:
                pass

    
    def reload_with_db(self):
        ...


    def __getitem__(self, __key: Any) -> Any:

        unique_default_identify = 'a450ec79-e2dd-4d90-af14-7d416a4c4316'

        value = self.get(__key, default=unique_default_identify)

        if value == unique_default_identify:
            raise KeyError(__key)
        
        return value
    


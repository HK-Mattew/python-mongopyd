import pymongo.errors
from mongopyd.async_document import AsyncDocument as Document
import asyncio
import pymongo
import bson



"""
.insert tests.
"""


def test_insert_allow_nulls():

    async def main():
    
        class MyModel(Document):
            
            class Settings():
                name = 'mymodel'
        

        doc = MyModel(
            null_value=None
        )

        
        result_insert = await doc.insert(allow_nulls=True)

        # print('doc =', doc)

        assert isinstance(result_insert, bson.ObjectId)


        # Find check value
        doc_found = await MyModel.find_one(
            filter={
                '_id': result_insert
            }
        )

        if doc_found:

            assert doc.get('null_value', 'my_default') is None

    asyncio.get_event_loop().run_until_complete(
        main()
    )


def test_insert_not_allow_nulls():
    
    async def main():

        class MyModel(Document):
            
            class Settings():
                name = 'mymodel'
        

        doc = MyModel(
            null_value=None
        )

        result_insert = await doc.insert(allow_nulls=False)

        # print('doc =', doc)

        assert isinstance(result_insert, bson.ObjectId)


        # Find check value
        doc_found = await MyModel.find_one(
            filter={
                '_id': result_insert
            }
        )

        if doc_found:

            assert doc_found.get('null_value', 'my_default') == 'my_default'


    asyncio.get_event_loop().run_until_complete(
        main()
    )



def test_insert_duplicate_key_error():
    

    async def main():
        class MyModel(Document):
            
            class Settings():
                name = 'mymodel'
        

        doc = MyModel(
            name='Ping and Pong'
        )

        await doc.insert()
        try:
            await doc.insert()
        except pymongo.errors.DuplicateKeyError:
            pass

    asyncio.get_event_loop().run_until_complete(
        main()
    )





"""
.find_one tests.
"""


def test_find_one_return_document_in_kwargs(
        ):
    
    async def main():
        class MyModel(Document):
            
            class Settings():
                name = 'mymodel'
        

        try:
            await MyModel.find_one(
                filter={},
                return_document=pymongo.ReturnDocument.AFTER
            )
        except ValueError as err:

            assert str(err) == 'You cannot use return_document as a parameter'

    asyncio.get_event_loop().run_until_complete(
        main()
    )




def test_find_one_filter_isinstance_of_objectid(
        ):
    

    async def main():
        class MyModel(Document):
            
            class Settings():
                name = 'mymodel'
        

        await MyModel.find_one(
            filter=bson.ObjectId()
        )

    asyncio.get_event_loop().run_until_complete(
        main()
    )


def test_find_one_filter_isinstance_of_str(
        ):
    

    async def main():
        class MyModel(Document):
            
            class Settings():
                name = 'mymodel'
        

        await MyModel.find_one(
            filter=str(bson.ObjectId())
        )

    asyncio.get_event_loop().run_until_complete(
        main()
    )



def test_find_one_with_update(
        ):
    
    async def main():
        class MyModel(Document):
            
            class Settings():
                name = 'mymodel'
        

        await MyModel.find_one(
            filter={},
            update={
                '$set': {
                    'name': 'Python'
                }
            }
        )

    asyncio.get_event_loop().run_until_complete(
        main()
    )



def test_find_one_result_is_none(
        ):
    
    async def main():
        class MyModel(Document):
            
            class Settings():
                name = 'mymodel'
        

        result = await MyModel.find_one(
            filter={
                '_id': bson.ObjectId()#Random ObjectID
            },
            update={}
        )

        assert result is None

    asyncio.get_event_loop().run_until_complete(
        main()
    )



def test_find_one_result_is_instance_of_model(
        ):
    
    async def main():
        class MyModel(Document):
            
            class Settings():
                name = 'mymodel'
        

        result = await MyModel.find_one(
            filter={},
            update={}
        )

        assert isinstance(result, MyModel)

    asyncio.get_event_loop().run_until_complete(
        main()
    )

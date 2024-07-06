import pymongo.errors
from mongopyd.sync_document import Document
import pymongo
import bson



"""
.insert tests.
"""


def test_insert_allow_nulls():
    
    class MyModel(Document):
        
        class Settings():
            name = 'mymodel'
    

    doc = MyModel(
        null_value=None
    )

    
    result_insert = doc.insert(allow_nulls=True)

    # print('doc =', doc)

    assert isinstance(result_insert, bson.ObjectId)


    # Find check value
    doc_found = MyModel.find_one(
        filter={
            '_id': result_insert
        }
    )

    if doc_found:

        assert doc.get('null_value', 'my_default') is None


def test_insert_not_allow_nulls():
    
    class MyModel(Document):
        
        class Settings():
            name = 'mymodel'
    

    doc = MyModel(
        null_value=None
    )

    result_insert = doc.insert(allow_nulls=False)

    # print('doc =', doc)

    assert isinstance(result_insert, bson.ObjectId)


    # Find check value
    doc_found = MyModel.find_one(
        filter={
            '_id': result_insert
        }
    )

    if doc_found:

        assert doc_found.get('null_value', 'my_default') == 'my_default'



def test_insert_duplicate_key_error():
    
    class MyModel(Document):
        
        class Settings():
            name = 'mymodel'
    

    doc = MyModel(
        name='Ping and Pong'
    )

    doc.insert()
    try:
        doc.insert()
    except pymongo.errors.DuplicateKeyError:
        pass





"""
.find_one tests.
"""


def test_find_one_return_document_in_kwargs(
        ):
    

    class MyModel(Document):
        
        class Settings():
            name = 'mymodel'
    

    try:
        MyModel.find_one(
            filter={},
            return_document=pymongo.ReturnDocument.AFTER
        )
    except ValueError as err:

        assert str(err) == 'You cannot use return_document as a parameter'




def test_find_one_filter_isinstance_of_objectid(
        ):
    

    class MyModel(Document):
        
        class Settings():
            name = 'mymodel'
    

    MyModel.find_one(
        filter=bson.ObjectId()
    )


def test_find_one_filter_isinstance_of_str(
        ):
    

    class MyModel(Document):
        
        class Settings():
            name = 'mymodel'
    

    MyModel.find_one(
        filter=str(bson.ObjectId())
    )



def test_find_one_with_update(
        ):
    

    class MyModel(Document):
        
        class Settings():
            name = 'mymodel'
    

    MyModel.find_one(
        filter={},
        update={
            '$set': {
                'name': 'Python'
            }
        }
    )



def test_find_one_result_is_none(
        ):
    

    class MyModel(Document):
        
        class Settings():
            name = 'mymodel'
    

    result = MyModel.find_one(
        filter={
            '_id': bson.ObjectId()#Random ObjectID
        },
        update={}
    )

    assert result is None



def test_find_one_result_is_instance_of_model(
        ):
    

    class MyModel(Document):
        
        class Settings():
            name = 'mymodel'
    

    result = MyModel.find_one(
        filter={},
        update={}
    )

    assert isinstance(result, MyModel)

from mongopyd.embedded_document import EmbeddedDocument




def test_get():
    
    doc = EmbeddedDocument(
        ping='pong',
        pong='ping'
    )


    assert doc.get('ping') == 'pong'
    assert doc.get('pong') == 'ping'



def test_get_key_id():
    
    doc = EmbeddedDocument(
        _id='12345',
        ping='pong',
        pong='ping'
    )


    assert doc.get('id') == '12345'



def test_get_key_with_pointers():
    
    doc = EmbeddedDocument(
        _id='12345',
        my_data={
            'foo': 'bar'
        }
    )


    assert doc.get('my_data.foo') == 'bar'



def test_get_key_with_pointers_not_dict_field():
    
    doc = EmbeddedDocument(
        _id='12345',
        my_data='bar'
    )


    try:
        assert doc.get('my_data.foo') == 'bar'
    except ValueError:
        pass



def test_get_key_with_pointers_dict_and_dict_field():
    
    doc = EmbeddedDocument(
        _id='12345',
        my_data={
            'foo': {
                'name': 'bar'
            }
        }
    )


    assert doc.get('my_data.foo.name') == 'bar'



def test_get_key_with_pointers_dict_and_dict_and_not_last_field():
    
    doc = EmbeddedDocument(
        _id='12345',
        my_data={
            'foo': 'bar'
        }
    )


    try:
        assert doc.get('my_data.foo.name.last_field') == 'bar'
    except ValueError:
        pass




def test___getitem__():

    doc = EmbeddedDocument(
        ping='pong',
        pong='ping'
    )


    assert doc['ping'] == 'pong'
    assert doc['pong'] == 'ping'



def test___getitem___key_error():

    doc = EmbeddedDocument(
        ping='pong',
        pong='ping'
    )

    try:
        doc['notfound']
        assert False
    except KeyError:
        pass


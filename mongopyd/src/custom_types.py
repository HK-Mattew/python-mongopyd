from typing_extensions import Annotated
from typing import Union, Any, Dict
from bson import ObjectId
from pydantic import (
    # PlainSerializer,
    AfterValidator,
    # WithJsonSchema
    )
import yaml




def func_validade_objectid(value: Any):

    if not isinstance(value, ObjectId):
        raise TypeError('ObjectId required')
    
    # if not ObjectId.is_valid(v):
    #     raise ValueError('Invalid ObjectId')

    return value



def func_validade_json_or_dict(value: Any):
    valid = None

    if not valid:
        if isinstance(value, dict):
            valid = True

    if not valid:
        try:
            value = yaml.load(value, Loader=yaml.Loader)
            valid = True
        except yaml.parser.ParserError:
            valid = False


    if not valid:
        raise ValueError("Invalid DICT/JSON")


    return value




PydanticObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(func_validade_objectid)
    # PlainSerializer(lambda x: str(x), return_type=str),
    # WithJsonSchema({"type": "string"}, mode="serialization")
]


JsonORDictField = Annotated[
    Union[str, Dict],
    AfterValidator(func_validade_json_or_dict)
]






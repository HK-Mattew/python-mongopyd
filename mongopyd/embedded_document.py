from pydantic import (
    BaseModel,
    Extra
)
from .src.custom_types import PydanticObjectId
from typing import (
    Any
)



class EmbeddedDocument(BaseModel):

    # Pydantic configs: https://docs.pydantic.dev/latest/usage/model_config/#options
    class Config():
        extra = Extra.allow
        json_encoders = {
            PydanticObjectId: lambda v: str(v),
        }



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



    def __getitem__(self, __key: Any) -> Any:

        unique_default_identify = 'a450ec79-e2dd-4d90-af14-7d416a4c4316'
        
        value = self.get(__key, default=unique_default_identify)

        if value == unique_default_identify:
            raise KeyError(__key)
        
        return value




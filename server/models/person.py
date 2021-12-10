from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson.objectid import ObjectId as BsonObjectId


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)


class AddressModel(BaseModel):
    street: str
    house: str
    apartment: str
    floor: Optional[int]
    landmark: Optional[str]


class PersonSchema(BaseModel):
    first_name: str
    last_name: str
    net_worth: int
    age: Optional[int]
    address: AddressModel


class PersonInDB(PersonSchema):
    id: PydanticObjectId


class UpdatePersonModel(BaseModel):
    first_name: str
    last_name: str
    net_worth: int
    age: Optional[int]
    address: AddressModel


class PartialUpdateModel(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    net_worth: Optional[int]
    age: Optional[int]
    address: Optional[AddressModel]


def ResponseModel(data, message):
    return {
        "data":[data],
        "code": 200,
        "message": message, 
    }


def ExtendedResponseModel(data, count, message):
    return {
        "data" : data,
        "count" : count,
        "code" : 200,
        "message": message
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message,
    }


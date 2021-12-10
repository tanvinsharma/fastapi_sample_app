import motor.motor_asyncio
import urllib
from bson.objectid import ObjectId
import pymongo
import json
from bson.json_util import dumps


client = pymongo.MongoClient("localhost", 27017)
# uncomment the line below to run locally
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb")



collection = client.db.crud_collection


def people_helper(person: dict) -> dict:
    return {
        "id": str(person["_id"]),
        "first_name": person["first_name"],
        "last_name": person["last_name"],
        "age": person["age"],
        "net_worth": person["net_worth"],
        "address": person["address"]
    }


async def retrieve_people():
    """
    Gets all the people in the db
    """
    people = []
    cursor = client.db.crud_collection.find({})

    for document in await cursor.to_list(length=100):
        people.append(dumps(document))

    return people


async def retrieve_people_limit(doc_limit: int, offset: int):
    """
    Similar function to retrieve_people. used for pagination
    """
    people = []
    cursor = client.db.crud_collection.find({}).skip(offset).limit(doc_limit)

    for document in await cursor.to_list(length=1000):
        people.append(dumps(document))

    return people


async def add_person(person_data: dict) -> dict:
    """
    Add new person in db
    """
    people = await client.db.crud_collection.insert_one(person_data)
    new_person = await client.db.crud_collection.find_one({"_id": people.inserted_id})
    return people_helper(new_person)


async def retrieve_person(id: ObjectId) -> dict:
    """
    Gets a person according to 'id'
    """
    try:
        person = await client.db.crud_collection.find_one({"_id": ObjectId(id)})
        if person:
            return people_helper(person)
    except Exception as e:
        return None

async def delete_all() -> bool:
    """
    Deletes all people in the db
    """
    await client.db.crud_collection.drop({})
    db_response = client.db.crud_collection.find({})

    if db_response:
        return 1
    else:
        return 0


async def update_person(id: str, data: dict) -> bool:
    """
    For updating a person with a given id
    Return False if an empty request body is sent.
    """
    if len(data) < 1:
        return False
    person = await client.db.crud_collection.find_one({"_id": ObjectId(id)})
    if person:
        updated_person = await client.db.crud_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_person:
            return True
        return False


async def get_total_count():
    """
    Function to get the total number of people in the db
    """
    count = await client.db.crud_collection.count_documents({})
    if count:
        return count
    else:
        return 0


async def delete_person(id: str):
    """
    Deletes a person form database if given id is found
    """
    person = await client.db.crud_collection.find_one({"_id": ObjectId(id)})
    if person:
        await client.db.crud_collection.delete_one({"_id": ObjectId(id)})
        return True

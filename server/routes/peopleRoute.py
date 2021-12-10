from fastapi import APIRouter, Body
from typing import Optional
from fastapi.encoders import jsonable_encoder
from pprint import pprint
import json
import copy

from server.database import (
    add_person,
    delete_person,
    retrieve_person,
    retrieve_people,
    update_person,
    delete_all,
    retrieve_people_limit,
    get_total_count
)

from server.models.person import (
    ErrorResponseModel,
    ResponseModel,
    PersonSchema,
    PersonInDB,
    UpdatePersonModel,
    PartialUpdateModel,
    ExtendedResponseModel
)

PeopleRouter = APIRouter()

"""
Post: add person
"""
@PeopleRouter.post("/", response_description="Person data added into the database")
async def add_person_data(person: PersonSchema):
    try:
        person = jsonable_encoder(person)
        new_person: PersonInDB = await add_person(person)

        return ResponseModel(new_person, "Person added successfully.")
    except Exception as e:
        return ErrorResponseModel(
            e,
            500,
            "Something went terribly wrong, we'll help you asap!"
        )

"""
Get: to get all people, also includes limits and skip for pagination
"""
@PeopleRouter.get("/", response_description="Person retrieved")
async def get_people(skip:int = 0, limit:int = 0):
    # print("this one")
    # print(skip, limit)
    try:
        if (limit == 0 and skip == 0):
            people: PersonInDB = await retrieve_people()
            if people:
                return ResponseModel(people, "People data retrieved successfully")
            return ResponseModel(people, "Empty list returned")
        else:
            people: PersonInDB = await retrieve_people_limit(limit, skip)
            count: int = await get_total_count()
            # print(count)
            if people:
                return ExtendedResponseModel(people,
                                             count,
                                             "Limit People data retrieved successfully")
            return ResponseModel(people, "Empty list returned")
    except Exception as e:
        print(e)
        return ErrorResponseModel(
            e,
            500,
            "Something went terribly wrong, we'll help you asap!"
        )

"""
Get: To get a persons data using their id
"""
@PeopleRouter.get("/{id}", response_description="Person data retrieved")
async def get_person_data(id):

    try:
        person: PersonInDB = await retrieve_person(id)
        if person:
            return ResponseModel(person, "Person data retrieved successfully")
        return ErrorResponseModel("An error occurred.", 404, "Person doesn't exist.")
    except KeyError as e:

        return ErrorResponseModel(
            e,
            500,
            "Something went terribly wrong, we'll help you asap!"
        )

"""
Put: To update a persons data
"""
@PeopleRouter.put("/{id}")
async def update_person_data(id: str, req: UpdatePersonModel):

        req = {k: v for k, v in req.dict().items() if v is not None}

        updated_person: PersonInDB = await update_person(id, req)
        if updated_person:
            return ResponseModel(
                "Person with ID: {} name update is successful".format(id),
                "Person name updated successfully",
            )
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error updating the person data.",
        )

"""
Delete: To delete a person from the db as per the given id
"""
@PeopleRouter.delete("/{id}", response_description="Person data deleted from the database")
async def delete_person_data(id: str):
    deleted_person: PersonInDB = await delete_person(id)
    if deleted_person:
        return ResponseModel(
            "Person with ID: {} removed".format(
                id), "Person deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Person with id {0} doesn't exist".format(
            id)
    )


"""
Delete: To delete all the people
"""
@PeopleRouter.delete("/", response_description="everyone deleted")
async def delete_everything():
    db_response = await delete_all()
    if db_response:
        return ResponseModel(
            "Everything is deleted",
            "Deleted"
        )
    else:
        return ErrorResponseModel(
            "An error has occured",
            500,
            "Work seems to be done but no outcome"
        )

"""
Patch: Used for partial update of person.
"""
@PeopleRouter.patch("/{id}", response_description="person updated")
async def partial_update_person(id: str, req: PartialUpdateModel):
    old_person: PersonInDB = await retrieve_person(id)

    for k,v in req.dict().items():
        if v is not None:
            old_person.update({k:v})

    updated_person: PersonInDB = await update_person(id, old_person)

    if updated_person:
        return ResponseModel(
            "Person with ID: {} name update is successful".format(id),
            "Person name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the person data.",
    )



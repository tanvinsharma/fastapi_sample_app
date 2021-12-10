from fastapi import FastAPI
from server.routes.peopleRoute import PeopleRouter

app = FastAPI()
app.include_router(PeopleRouter, tags=["People"], prefix="/people")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello there people, add yourself :)"}


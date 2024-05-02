from fastapi.routing import APIRouter
from fastapi import Request

from schemas import UserSchema
from crud import crud_instance


create_user_router = APIRouter()

@create_user_router.post("/create_user", response_model=UserSchema)
async def answer_create_user(user_data: UserSchema) -> UserSchema:
    new_user_data = user_data.model_dump()
    await crud_instance.create_user_db(**new_user_data)
    return new_user_data

# curl -X POST "http://127.0.0.1.:8000/create_user" -H "Content-Type: application/json" -d '{"env": "stage", "login": "1222", "password": "1", "domain": "regular", "project_id": "44a842a7-6675-41fd-b1e1-291896a2f9fb"}'

from fastapi.routing import APIRouter
from schemas import UserSchema
from crud import crud_instance

from typing import List

get_users_router = APIRouter()

@get_users_router.get("/get_users", response_model=List[UserSchema])
async def answer_get_users() -> list[UserSchema]:
    users = await crud_instance.get_users_db()
    return users

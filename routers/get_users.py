from fastapi.routing import APIRouter
from models import User
from crud import CRUD

from typing import List

get_users_router = APIRouter()
crud_ex = CRUD()

@get_users_router.get("/get_users", response_model=List[User])
async def answer_get_users() -> list[dict]:
    users = await crud_ex.get_users_db()
    return users
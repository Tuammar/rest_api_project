from fastapi.routing import APIRouter
from models import LockRelease
from crud import CRUD

release_lock_router = APIRouter()
crud_ex = CRUD()

@release_lock_router.post("/release_lock")
async def answer_release_lock(lock_data: LockRelease) -> dict:
    lock_result = await crud_ex.lock_release_db(lock_data.login, lock_data.password)
    if lock_result:
        return lock_result
    else:
        return {'user': lock_data.login, 'status': 'user not found'}
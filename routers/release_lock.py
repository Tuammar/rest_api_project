from fastapi.routing import APIRouter
from schemas import LockReleaseSchema
from crud import crud_instance
from schemas import LockSchema

release_lock_router = APIRouter()


@release_lock_router.post("/release_lock")
async def answer_release_lock(lock_data: LockReleaseSchema) -> LockSchema:
    lock_result = await crud_instance.lock_release_db(lock_data.user_id)
    if lock_result:
        return lock_result
    else:
        return {"user": lock_data.user_id, "status": "user not found"}

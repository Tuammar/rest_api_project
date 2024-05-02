from fastapi.routing import APIRouter
from schemas import LockAcquisitionSchema, LockSchema
from crud import crud_instance
from time import time

acquire_lock_router = APIRouter()

@acquire_lock_router.post("/acquire_lock")
async def answer_acquire_lock(lock_data: LockAcquisitionSchema) -> LockSchema:
    lock_result = await crud_instance.lock_acquire_db(lock_data.user_id, time())
    if lock_result:
        return lock_result
    else:
        return {'user': lock_data.user_id, 'status': 'user not found'}
    
    # curl -X POST "http://127.0.0.1.:8000/acquire_lock" -H "Content-Type: application/json" -d '{"login": "1234", "password": "4321", "project_id": "123e4567-e89b-12d3-a456-426614174000"}'

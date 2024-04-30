from fastapi.routing import APIRouter
from models import LockAcquisition
from crud import CRUD
from time import time

acquire_lock_router = APIRouter()
crud_ex = CRUD()

@acquire_lock_router.post("/acquire_lock")
async def answer_acquire_lock(lock_data: LockAcquisition) -> dict:
    lock_result = await crud_ex.lock_acquire_db(lock_data.login, lock_data.password, lock_data.project_id, time())
    if lock_result:
        return lock_result
    else:
        return {'user': lock_data.login, 'status': 'user not found'}
    
    # curl -X POST "http://127.0.0.1.:8000/acquire_lock" -H "Content-Type: application/json" -d
    # '{"login": "1234", "password": "4321", "project_id": "123e4567-e89b-12d3-a456-426614174000"}'
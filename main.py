import uvicorn
from fastapi import FastAPI
from routers.ping import ping_router
from routers.create_user import create_user_router
from routers.get_users import get_users_router
from routers.acquire_lock import acquire_lock_router
from routers.release_lock import release_lock_router

app = FastAPI(title="REST API")

app.include_router(ping_router)
app.include_router(create_user_router)
app.include_router(get_users_router)
app.include_router(acquire_lock_router)
app.include_router(release_lock_router)



if __name__ == "__main__":
    print('running uvicorn')
    uvicorn.run(app, host="0.0.0.0", port=8000)
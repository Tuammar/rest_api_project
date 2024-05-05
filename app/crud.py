from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from models import Base
from datetime import date
from models import User
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from schemas import UserSchema, LockSchema
import os

"""crud.py содержит класс CRUD, обеспечивающий
взаимодействие с базой данных"""


class CRUD:
    def __init__(self):
        # при инициализации создается асинхронная сессия
        self.engine = create_async_engine(os.environ["DATABASE_URL"])
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def create_table(self):
        # функция создания таблицы users
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create_user_db(
        self,
        user_id: UUID,
        created_ad: date,
        login: str,
        password: str,
        project_id: UUID,
        env: str,
        domain: str,
        locktime: float,
    ) -> UserSchema:
        # функция добавления нового пользователя в базу данных
        async with self.async_session() as session:
            new_user = User(
                user_id=user_id,
                created_ad=created_ad,
                login=login,
                password=bcrypt.hash(password),
                project_id=project_id,
                env=env,
                domain=domain,
                locktime=locktime,
            )
            try:
                session.add(new_user)
                await session.commit()
                return new_user
            except IntegrityError:
                await session.rollback()
                return {"error": "IntegrityError"}

    async def get_users_db(self) -> list[UserSchema]:
        # функция получения пользователей из базы данных
        async with self.async_session() as session:
            stmt = select(User)
            select_result = await session.execute(stmt)
            final_result = []
            for i in select_result:
                selected_user = i[0]
                user_data = {
                    "user_id": selected_user.user_id,
                    "created_ad": selected_user.created_ad,
                    "login": selected_user.login,
                    "password": selected_user.password,
                    "project_id": selected_user.project_id,
                    "env": selected_user.env,
                    "domain": selected_user.domain,
                    "locktime": selected_user.locktime,
                }
                final_result.append(user_data)
            return final_result

    async def get_user_by_user_id(self, user_id) -> UserSchema:
        # функция получения пользователя по user_id
        async with self.async_session() as session:
            stmt = select(User).where(User.user_id == user_id)
            selected_user = await session.execute(stmt)
            selected_user = selected_user.fetchone()[0]
            user_data = {
                "user_id": selected_user.user_id,
                "created_ad": selected_user.created_ad,
                "login": selected_user.login,
                "password": selected_user.password,
                "project_id": selected_user.project_id,
                "env": selected_user.env,
                "domain": selected_user.domain,
                "locktime": selected_user.locktime,
            }
            return user_data

    async def user_locktime_db(self, user_id: UUID):
        # функция получения locktime пользователя по id
        async with self.async_session():
            user = await self.get_user_by_user_id(user_id)
            return user["locktime"]

    async def lock_acquire_db(self, user_id: UUID, locktime: float) -> LockSchema:
        # функция блокировки пользователя
        async with self.async_session() as session:
            try:
                if await self.user_locktime_db(user_id) != 0.0:
                    return {"user": user_id, "status": "user had already been locked"}
                stmt = (
                    update(User)
                    .where(User.user_id == user_id and User.locktime == 0.0)
                    .values(locktime=locktime)
                )
                await session.execute(stmt)
                await session.commit()
                return {"user": user_id, "locktime": locktime, "status": "done"}
            except Exception:
                return {"user": user_id, "status": "error"}

    async def lock_release_db(self, user_id: UUID) -> LockSchema:
        # функция снятия блокировки с пользователя по user_id
        async with self.async_session() as session:
            try:
                if await self.user_locktime_db(user_id) == 0.0:
                    return {"user": user_id, "status": "user had already been free"}
                stmt = update(User).where(User.user_id == user_id).values(locktime=0.0)
                await session.execute(stmt)
                await session.commit()
                return {"user": user_id, "locktime": 0.0, "status": "done"}
            except Exception:
                return {"user": user_id, "locktime": None, "status": "error"}


crud_instance = CRUD()

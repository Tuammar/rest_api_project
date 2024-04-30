from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from database_models import Base
from datetime import date
from database_models import UsersTable
from sqlalchemy.exc import IntegrityError, NoResultFound
from passlib.hash import bcrypt


class CRUD:
    def __init__(self):
        self.engine = create_async_engine("postgresql+asyncpg://postgres:123@localhost/prof_zadaniye", echo=True)
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_user_db(self, user_id: UUID, created_ad: date, login: str, password: str,
                        project_id: UUID, env: str, domain: str, locktime: float):
        async with self.async_session() as session:
            new_user = UsersTable(user_id=user_id, created_ad=created_ad, login=login, password=bcrypt.hash(password),
                                    project_id=project_id, env=env,
                                    domain=domain, locktime=locktime)
            try:
                session.add(new_user)
                await session.commit()
                return {user_id, created_ad, login, password,
                        project_id, env, domain, locktime}
            except IntegrityError as e:
                await session.rollback()
                print(e)
    
    async def get_users_db(self) -> list[dict]:
        async with self.async_session() as session:
            stmt = select(UsersTable)
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
    
    # async def get_user_by_id(self, uid) -> list[dict]:
    #     async with self.async_session() as session:
    #         stmt = select(UsersTable).where(UsersTable.user_id == uid)
    #         selected_user = await session.execute(stmt)
    #         selected_user = selected_user.fetchone()[0]
    #         user_data = {
    #             "user_id": selected_user.user_id,
    #             "created_ad": selected_user.created_ad,
    #             "login": selected_user.login,
    #             "password": selected_user.password,
    #             "project_id": selected_user.project_id,
    #             "env": selected_user.env,
    #             "domain": selected_user.domain,
    #             "locktime": selected_user.locktime
    #             }
    #         return user_data
    
    async def get_user_by_login(self, login) -> list[dict]:
        async with self.async_session() as session:
            stmt = select(UsersTable).where(UsersTable.login == login)
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
                "locktime": selected_user.locktime
                }
            return user_data
    
    async def lock_acquire_db(self, login: str, password: str, project_id: UUID, locktime: float) -> dict:
        async with self.async_session() as session:
            try:
                user = await self.get_user_by_login(login)
                if bcrypt.verify(password.encode('utf-8'), user['password'].encode('utf-8')):
                    stmt = update(UsersTable).where(UsersTable.login == login).\
                        values(project_id=project_id, locktime=locktime)
                    await session.execute(stmt)
                    await session.commit()
                    return {'user': login, 'project_id': project_id, 'locktime': locktime, 'status': 'done'}
            except Exception as e:
                return {'error': e}

    async def lock_release_db(self, login: str, password: str) -> dict:
        async with self.async_session() as session:
            try:
                user = await self.get_user_by_login(login)
                if bcrypt.verify(password.encode('utf-8'), user['password'].encode('utf-8')):
                    stmt = update(UsersTable).where(UsersTable.login == login).\
                        values(locktime=0.0)
                    await session.execute(stmt)
                    await session.commit()
                    return {'user': login, 'locktime': 0.0, 'status': 'done'}
            except Exception as e:
                return {'error': e}
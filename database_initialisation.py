from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database_models import Base
from uuid import UUID
import asyncio


engine = create_async_engine("postgresql+asyncpg://postgres:123@localhost/prof_zadaniye", future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_table())
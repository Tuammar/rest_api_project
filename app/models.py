from sqlalchemy import Column, String, Date, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

"""в models.py задан класс User - описание
структуры таблицы users, в которой
хранятся данные о пользователях"""

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    created_ad = Column(Date)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    project_id = Column(UUID(as_uuid=True))
    env = Column(String)
    domain = Column(String)
    locktime = Column(Float)

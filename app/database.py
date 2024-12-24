from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from functools import lru_cache

from .config import Settings



@lru_cache()
def get_settings():
    return Settings()


host = get_settings().host
username = get_settings().username
password = get_settings().password
database = get_settings().database
port = get_settings().port


DATABASE_URL = f'postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}'


Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

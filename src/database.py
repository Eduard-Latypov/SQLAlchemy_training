from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from src.config import Settings

settings = Settings()


sync_engine = create_engine(settings.sync_url)
async_engine = create_async_engine(settings.async_url)

sync_session = sessionmaker(sync_engine)
async_session = async_sessionmaker(async_engine)

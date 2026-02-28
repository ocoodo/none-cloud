from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends

from settings import settings


engine = create_async_engine(settings.db_url)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


DbSession = Annotated[AsyncSession, Depends(get_session)]

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db


async def get_async_db() -> AsyncSession:
    async for session in get_db():
        yield session

import asyncio
from app.database.models import User, Category, Product, CartItem, WishlistItem, Address, Order, OrderItem
from app.database.database import AsyncSessionLocal, init_db
from sqlalchemy import text

async def main():
    await init_db()
    async with AsyncSessionLocal() as db:
        result = await db.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"))
        print(result.all())

asyncio.run(main())

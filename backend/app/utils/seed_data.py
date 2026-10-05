from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.database.models import Category, Product, User


async def seed_demo_data(db: AsyncSession) -> None:
    category_result = await db.execute(select(Category))
    if not category_result.scalars().first():
        categories = [
            Category(name="Electronics", description="Smart devices and gadgets", image_url="https://images.unsplash.com/photo-1518770660439-463ac2bf7e3d"),
            Category(name="Home", description="Home essentials", image_url="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85"),
            Category(name="Fashion", description="Style and accessories", image_url="https://images.unsplash.com/photo-1521572267360-ee0c2909d518"),
        ]
        db.add_all(categories)
        await db.commit()

    user_result = await db.execute(select(User).where(User.email == "admin@smartcart.local"))
    if not user_result.scalar_one_or_none():
        admin = User(
            full_name="Admin User",
            email="admin@smartcart.local",
            password_hash=get_password_hash("admin123"),
            phone="5550001",
            role="admin",
            is_active=True,
        )
        db.add(admin)
        await db.commit()

    product_result = await db.execute(select(Product))
    if not product_result.scalars().first():
        categories = (await db.execute(select(Category))).scalars().all()
        by_name = {category.name: category for category in categories}
        products = [
            Product(name="Smart Speaker Pro", description="Premium voice assistant", price=129.99, discount_percentage=10, stock_quantity=25, brand="Echo", image_url="https://images.unsplash.com/photo-1546435770-a3e426bf472b", category_id=by_name["Electronics"].id, rating=4.8),
            Product(name="Minimal Desk Lamp", description="Warm lighting for home office", price=49.99, discount_percentage=15, stock_quantity=18, brand="Nord", image_url="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85", category_id=by_name["Home"].id, rating=4.6),
            Product(name="Classic Leather Backpack", description="Everyday carry", price=89.99, discount_percentage=12, stock_quantity=22, brand="Cove", image_url="https://images.unsplash.com/photo-1521572267360-ee0c2909d518", category_id=by_name["Fashion"].id, rating=4.7),
        ]
        db.add_all(products)
        await db.commit()
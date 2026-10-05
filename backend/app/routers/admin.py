from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_admin
from app.database.database import get_db
from app.database.models import Order, Product, User

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/dashboard")
async def dashboard(current_admin: User = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    user_total = await db.scalar(select(func.count()).select_from(User))
    product_total = await db.scalar(select(func.count()).select_from(Product))
    order_total = await db.scalar(select(func.count()).select_from(Order))
    revenue_total = await db.scalar(select(func.coalesce(func.sum(Order.final_amount), 0.0)).select_from(Order))
    return {
        "total_users": int(user_total or 0),
        "total_products": int(product_total or 0),
        "total_orders": int(order_total or 0),
        "total_revenue": float(revenue_total or 0.0),
    }


@router.get("/users")
async def list_users(current_admin: User = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).order_by(User.id))
    return [
        {"id": user.id, "full_name": user.full_name, "email": user.email, "role": user.role, "is_active": user.is_active}
        for user in result.scalars().all()
    ]


@router.get("/orders")
async def list_admin_orders(current_admin: User = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).order_by(Order.created_at.desc()))
    return [
        {"id": order.id, "user_id": order.user_id, "order_status": order.order_status, "payment_status": order.payment_status, "final_amount": order.final_amount}
        for order in result.scalars().all()
    ]


@router.get("/inventory")
async def inventory_overview(current_admin: User = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).order_by(Product.id))
    return [
        {"id": product.id, "name": product.name, "price": product.price, "stock_quantity": product.stock_quantity, "is_active": product.is_active}
        for product in result.scalars().all()
    ]
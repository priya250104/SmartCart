from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.database.database import get_db
from app.database.models import Address, CartItem, Order, OrderItem, User

router = APIRouter(prefix="/api", tags=["orders"])


@router.get("/orders")
async def list_orders(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.user_id == current_user.id).order_by(Order.created_at.desc()))
    orders = result.scalars().all()
    payload = []
    for order in orders:
        payload.append({
            "id": order.id,
            "order_status": order.order_status,
            "payment_status": order.payment_status,
            "final_amount": order.final_amount,
            "items": [{
                "id": item.id,
                "product_name": item.product_name,
                "product_price": item.product_price,
                "quantity": item.quantity,
                "subtotal": item.subtotal,
            } for item in order.order_items],
        })
    return payload


@router.get("/orders/{order_id}")
async def get_order(order_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == order_id, Order.user_id == current_user.id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "id": order.id,
        "order_status": order.order_status,
        "payment_status": order.payment_status,
        "final_amount": order.final_amount,
        "items": [{
            "id": item.id,
            "product_name": item.product_name,
            "product_price": item.product_price,
            "quantity": item.quantity,
            "subtotal": item.subtotal,
        } for item in order.order_items],
    }


@router.post("/orders")
async def create_order(payload: dict, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    address_id = payload.get("address_id")
    if not address_id:
        raise HTTPException(status_code=400, detail="address_id is required")

    address_result = await db.execute(select(Address).where(Address.id == address_id, Address.user_id == current_user.id))
    address = address_result.scalar_one_or_none()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    cart_result = await db.execute(select(CartItem).where(CartItem.user_id == current_user.id).order_by(CartItem.id))
    items = cart_result.scalars().all()
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0.0
    order_items = []
    for cart_item in items:
        product = cart_item.product
        if not product or product.stock_quantity < cart_item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name if product else 'product'}")

        subtotal = product.price * cart_item.quantity
        total += subtotal
        order_items.append({
            "product_id": product.id,
            "product_name": product.name,
            "product_price": product.price,
            "quantity": cart_item.quantity,
            "subtotal": subtotal,
        })

    order = Order(
        user_id=current_user.id,
        total_amount=total,
        shipping_amount=0.0,
        discount_amount=0.0,
        final_amount=total,
        payment_status="pending",
        order_status="placed",
        shipping_address=f"{address.full_name}, {address.address_line1}, {address.city}, {address.state}, {address.country}",
    )
    db.add(order)
    await db.flush()

    for item in order_items:
        db.add(OrderItem(order_id=order.id, **item))

    for cart_item in items:
        if cart_item.product:
            cart_item.product.stock_quantity -= cart_item.quantity

    await db.execute(delete(CartItem).where(CartItem.user_id == current_user.id))
    await db.commit()
    await db.refresh(order)
    return {"id": order.id, "payment_status": order.payment_status, "order_status": order.order_status, "final_amount": order.final_amount}


@router.post("/orders/{order_id}/cancel")
async def cancel_order(order_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == order_id, Order.user_id == current_user.id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.order_status = "cancelled"
    await db.commit()
    return {"cancelled": True, "order_id": order.id}
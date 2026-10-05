from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.database.models import CartItem, Product, User
from app.core.security import get_current_user
from app.schemas.schemas import CartItemCreate, CartItemOut, CartItemUpdate

router = APIRouter(prefix="/api", tags=["cart"])


@router.get("/cart", response_model=dict)
async def get_cart(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CartItem).where(CartItem.user_id == current_user.id).order_by(CartItem.id))
    items = result.scalars().all()
    payload = []
    total = 0.0
    for item in items:
        subtotal = item.quantity * item.product.price
        total += subtotal
        payload.append({
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "subtotal": subtotal,
            "product": {
                "id": item.product.id,
                "name": item.product.name,
                "price": item.product.price,
                "brand": item.product.brand,
                "image_url": item.product.image_url,
            },
        })
    return {"items": payload, "total": total}


@router.post("/cart", response_model=dict)
async def add_cart_item(payload: CartItemCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    product_result = await db.execute(select(Product).where(Product.id == payload.product_id))
    product = product_result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock_quantity < payload.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    existing = await db.execute(select(CartItem).where(CartItem.user_id == current_user.id, CartItem.product_id == payload.product_id))
    item = existing.scalar_one_or_none()
    if item:
        item.quantity += payload.quantity
    else:
        item = CartItem(user_id=current_user.id, product_id=payload.product_id, quantity=payload.quantity)
        db.add(item)

    await db.commit()
    await db.refresh(item)
    return {"added": True, "item_id": item.id}


@router.patch("/cart/{item_id}", response_model=dict)
async def update_cart_item(item_id: int, payload: CartItemUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CartItem).where(CartItem.id == item_id, CartItem.user_id == current_user.id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    item.quantity = payload.quantity
    await db.commit()
    return {"updated": True}


@router.delete("/cart/{item_id}")
async def remove_cart_item(item_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CartItem).where(CartItem.id == item_id, CartItem.user_id == current_user.id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    await db.delete(item)
    await db.commit()
    return {"removed": True}


@router.delete("/cart")
async def clear_cart(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(select(CartItem).where(CartItem.user_id == current_user.id).delete())
    await db.commit()
    return {"cleared": True}

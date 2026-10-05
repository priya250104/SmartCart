from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.database.database import get_db
from app.database.models import Product, User, WishlistItem

router = APIRouter(prefix="/api", tags=["wishlist"])


@router.get("/wishlist")
async def get_wishlist(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WishlistItem).where(WishlistItem.user_id == current_user.id).order_by(WishlistItem.id))
    rows = result.scalars().all()
    items = []
    for row in rows:
        items.append({
            "id": row.id,
            "product_id": row.product_id,
            "product": {
                "id": row.product.id,
                "name": row.product.name,
                "price": row.product.price,
                "brand": row.product.brand,
                "image_url": row.product.image_url,
            },
        })
    return items


@router.post("/wishlist")
async def add_wishlist_item(product_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    product_result = await db.execute(select(Product).where(Product.id == product_id))
    product = product_result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = await db.execute(select(WishlistItem).where(WishlistItem.user_id == current_user.id, WishlistItem.product_id == product_id))
    if existing.scalar_one_or_none():
        return {"added": False, "message": "Already in wishlist"}

    item = WishlistItem(user_id=current_user.id, product_id=product_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return {"added": True, "item_id": item.id}


@router.delete("/wishlist/{product_id}")
async def remove_wishlist_item(product_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WishlistItem).where(WishlistItem.user_id == current_user.id, WishlistItem.product_id == product_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    await db.delete(item)
    await db.commit()
    return {"removed": True}
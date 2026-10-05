from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.database.database import get_db
from app.database.models import Address, User
from app.schemas.schemas import AddressCreate, AddressOut, AddressUpdate

router = APIRouter(prefix="/api", tags=["addresses"])


@router.get("/addresses", response_model=list[AddressOut])
async def get_addresses(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Address).where(Address.user_id == current_user.id).order_by(Address.id))
    return result.scalars().all()


@router.post("/addresses", response_model=AddressOut)
async def create_address(payload: AddressCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if payload.is_default:
        await db.execute(
            "UPDATE addresses SET is_default = false WHERE user_id = :uid",
            {"uid": current_user.id},
        )
    address = Address(user_id=current_user.id, **payload.model_dump())
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address


@router.patch("/addresses/{address_id}", response_model=AddressOut)
async def update_address(address_id: int, payload: AddressUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Address).where(Address.id == address_id, Address.user_id == current_user.id))
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(address, field, value)
    await db.commit()
    await db.refresh(address)
    return address


@router.delete("/addresses/{address_id}")
async def delete_address(address_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Address).where(Address.id == address_id, Address.user_id == current_user.id))
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    await db.delete(address)
    await db.commit()
    return {"deleted": True}
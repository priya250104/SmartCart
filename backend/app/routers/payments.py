from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.database.database import get_db
from app.database.models import Order, User
from app.schemas.schemas import PaymentOut, PaymentVerify

router = APIRouter(prefix="/api", tags=["payments"])


@router.post("/payments/verify", response_model=PaymentOut)
async def verify_payment(payload: PaymentVerify, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == payload.order_id, Order.user_id == current_user.id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if payload.success:
        order.payment_status = "paid"
        order.order_status = "confirmed"
        message = "Payment verified"
        status_value = "success"
    else:
        order.payment_status = "failed"
        message = "Payment failed"
        status_value = "failed"

    await db.commit()
    return {"order_id": order.id, "status": status_value, "payment_method": payload.payment_method, "message": message}
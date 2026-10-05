from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseSchema):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str = "customer"


class UserCreate(BaseSchema):
    full_name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None


class UserLogin(BaseSchema):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool = True
    created_at: Optional[datetime] = None


class Token(BaseSchema):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseSchema):
    sub: str


class CategoryCreate(BaseSchema):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None


class CategoryOut(CategoryCreate):
    id: int


class ProductBase(BaseSchema):
    name: str
    description: Optional[str] = None
    price: float = Field(ge=0)
    discount_percentage: float = Field(default=0.0, ge=0, le=100)
    stock_quantity: int = Field(default=0, ge=0)
    brand: Optional[str] = None
    image_url: Optional[str] = None
    category_id: int
    rating: float = Field(default=0.0, ge=0, le=5)
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    discount_percentage: Optional[float] = Field(default=None, ge=0, le=100)
    stock_quantity: Optional[int] = Field(default=None, ge=0)
    brand: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    is_active: Optional[bool] = None


class ProductOut(ProductBase):
    id: int
    category: Optional[CategoryOut] = None


class CartItemCreate(BaseSchema):
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemUpdate(BaseSchema):
    quantity: int = Field(ge=1)


class CartProductOut(BaseSchema):
    id: int
    name: str
    price: float
    image_url: Optional[str] = None
    brand: Optional[str] = None


class CartItemOut(BaseSchema):
    id: int
    product_id: int
    quantity: int
    subtotal: float
    product: Optional[CartProductOut] = None


class WishlistItemOut(BaseSchema):
    id: int
    product_id: int
    product: Optional[CartProductOut] = None


class AddressCreate(BaseSchema):
    full_name: str
    phone: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str
    is_default: bool = False


class AddressUpdate(AddressCreate):
    pass


class AddressOut(AddressCreate):
    id: int
    user_id: int
    is_default: bool


class OrderItemOut(BaseSchema):
    id: int
    product_id: Optional[int]
    product_name: str
    product_price: float
    quantity: int
    subtotal: float


class OrderCreate(BaseSchema):
    address_id: int
    payment_method: str = "cod"


class OrderOut(BaseSchema):
    id: int
    user_id: int
    total_amount: float
    shipping_amount: float
    discount_amount: float
    final_amount: float
    payment_status: str
    order_status: str
    shipping_address: str
    created_at: Optional[datetime] = None
    items: List[OrderItemOut] = []


class PaymentVerify(BaseSchema):
    order_id: int
    payment_method: str = "cod"
    success: bool = True


class PaymentOut(BaseSchema):
    order_id: int
    status: str
    payment_method: str
    message: str


class DashboardStats(BaseSchema):
    total_users: int
    total_products: int
    total_orders: int
    total_revenue: float


class ProductListResponse(BaseSchema):
    items: List[ProductOut]
    total: int
    page: int
    page_size: int

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.database import AsyncSessionLocal, init_db
from app.routers import admin, addresses, auth, cart, orders, payments, products, wishlist
from app.utils.seed_data import seed_demo_data

app = FastAPI(title="SmartCart", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    await init_db()
    async with AsyncSessionLocal() as session:
        await seed_demo_data(session)


@app.get("/")
async def root() -> dict:
    return {"message": "SmartCart API is running"}


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(wishlist.router)
app.include_router(addresses.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(admin.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
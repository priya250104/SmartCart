# SmartCart

SmartCart is a production-style full-stack e-commerce application built with React, FastAPI, PostgreSQL, JWT authentication, and Docker.

## Overview

This project includes a customer storefront and an admin dashboard. Customers can browse products, add items to their cart and wishlist, manage addresses, place orders, and track order progress. Admins can manage products, categories, users, orders, and inventory.

## Features

- Customer registration and login with JWT authentication
- Product browsing, search, filtering, sorting, and pagination
- Wishlist, cart, and address management
- Checkout flow with order creation and stock validation
- Payment simulation with success/failure handling
- Order tracking and cancellation rules
- Admin dashboard with analytics and inventory insights
- PostgreSQL-ready backend with SQLAlchemy and Alembic
- Dockerized frontend, backend, and database
- Pytest coverage for important backend behavior

## Tech Stack

- Frontend: React, Vite, React Router, Axios, Context API, Recharts
- Backend: Python 3.11+, FastAPI, SQLAlchemy, Pydantic, JWT, Passlib
- Database: PostgreSQL, Alembic
- Containerization: Docker, Docker Compose

## Architecture

- Frontend in `frontend/`
- Backend in `backend/`
- Shared app configuration with environment files
- API integration via Axios with centralized service layer

## Project Structure

```text
smartcart/
├── frontend/
├── backend/
├── docker-compose.yml
├── .gitignore
├── README.md
└── ...
```

## Database Schema

The backend uses SQLAlchemy models for users, categories, products, cart items, wishlist items, addresses, orders, and order items.

## API Endpoints

Main endpoints include:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/products`
- `GET /api/products/{id}`
- `POST /api/products`
- `PUT /api/products/{id}`
- `DELETE /api/products/{id}`
- `GET /api/categories`
- `POST /api/categories`
- `PUT /api/categories/{id}`
- `DELETE /api/categories/{id}`
- `GET /api/cart`
- `POST /api/cart/items`
- `PUT /api/cart/items/{id}`
- `DELETE /api/cart/items/{id}`
- `GET /api/wishlist`
- `POST /api/wishlist/{product_id}`
- `DELETE /api/wishlist/{product_id}`
- `GET /api/addresses`
- `POST /api/addresses`
- `PUT /api/addresses/{id}`
- `DELETE /api/addresses/{id}`
- `POST /api/orders`
- `GET /api/orders`
- `GET /api/orders/{id}`
- `POST /api/orders/{id}/cancel`
- `GET /api/admin/dashboard`
- `GET /api/admin/orders`
- `PATCH /api/admin/orders/{id}/status`

## Authentication

Authentication uses JWT bearer tokens. Protected routes require the `Authorization: Bearer <token>` header. Role-based access is enforced for admin-only operations.

## Installation

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Environment Variables

Backend `.env` variables include:

```env
DATABASE_URL=postgresql+asyncpg://smartcart:smartcart123@localhost:5432/smartcart
SECRET_KEY=change_this_secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:5173
APP_ENV=development
```

Frontend `.env` variables include:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## Running with Docker

```bash
docker compose up --build
```

## Database Migration

```bash
cd backend
alembic upgrade head
```

To create new migrations:

```bash
cd backend
alembic revision --autogenerate -m "describe change"
```

## Seed Data

The backend includes a seed script that creates demo data for admin and customer accounts, categories, products, and sample inventory.

Default demo credentials:

- Admin: `admin@smartcart.com` / `Admin@123`
- Customer: `customer@smartcart.com` / `Customer@123`

## Testing

```bash
cd backend
pytest
```

## Screenshots

Add screenshots here after running the app locally.

## Future Improvements

- Add real payment gateway integration
- Add product review and ratings system
- Add inventory notifications and alerts
- Add advanced analytics dashboards
- Add shipping tracking integrations

## Author

SmartCart portfolio project



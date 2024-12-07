from dotenv import load_dotenv
from fastapi import FastAPI

from app.category.controller import app as category_router
from app.employee.controller import app as employee_router
from app.infra.server import lifespan
from app.order.controller import app as order_router
from app.product.controller import app as product_router

load_dotenv()


def create_app():
    app = FastAPI(
        title="BigBurger",
        version="v0.2.0",
        description="API REST for diner management.",
        lifespan=lifespan,
    )
    app.include_router(product_router)
    app.include_router(category_router)
    app.include_router(order_router)
    app.include_router(employee_router)
    return app

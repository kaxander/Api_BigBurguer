from fastapi import FastAPI

from app.category.controller import app as category_router
from app.config import get_settings
from app.employee.controller import app as employee_router
from app.infra.server import lifespan
from app.order.controller import app as order_router
from app.product.controller import app as product_router


def create_app():
    config = get_settings()
    app = FastAPI(
        title=config.title,
        version=config.version,
        description=config.description,
        lifespan=lifespan,
    )
    app.include_router(product_router)
    app.include_router(category_router)
    app.include_router(order_router)
    app.include_router(employee_router)
    return app

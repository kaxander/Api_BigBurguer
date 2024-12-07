from typing import Any

from app.infra.db import Session
from app.product import repository
from app.product.model import ProductModel
from app.product.schema import ProductCreateSchema, ProductSchema, ProductUpdateSchema


def get_product(session: Session, product_id: int) -> ProductSchema | None:
    try:
        product = repository.get(product_id=product_id, session=session)
        return ProductSchema(**product.__dict__)
    except BaseException:
        return None


def get_products(session: Session, **kwargs: Any) -> list[ProductSchema]:
    products = repository.get_all(session=session, **kwargs)
    return [ProductSchema(**p.__dict__) for p in products]


def remove_product(session: Session, product_id: int) -> bool:
    with session.begin():
        repository.delete(product_id=product_id, session=session)
    return True


def save_product(session: Session, product: ProductCreateSchema) -> ProductSchema:
    with session.begin():
        product_created = repository.create(session=session, product=ProductModel(**product.__dict__))
        product_ = ProductSchema(**product_created.__dict__)
    return product_


def update_product(
    session: Session, product_id: int, product: ProductUpdateSchema | ProductCreateSchema
) -> ProductSchema:
    with session.begin():
        product_updated = repository.update(session=session, product_id=product_id, **product.__dict__)
        product_ = ProductSchema(**product_updated.__dict__)
    return product_

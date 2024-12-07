from typing import Any

from app.infra.db import Session
from app.product.model import ProductModel


def get(session: Session, product_id: int) -> ProductModel:
    return session.query(ProductModel).filter(ProductModel.id == product_id).one()

def get_all(session: Session, **kwargs: Any) -> list[ProductModel]:
    return session.query(ProductModel).filter_by(**kwargs).all()

def delete(session: Session, product_id: int) -> None:
    m = get(session=session, product_id=product_id)
    return session.delete(m)

def create(session: Session, product: ProductModel) -> ProductModel:
    session.add(product)
    session.flush()
    return product
    
def update(session: Session, product_id: int, **kwargs: Any) -> ProductModel:
    m = get(session=session, product_id=product_id)
    for k, v in kwargs.items():
        setattr(m, k, v)
    return m

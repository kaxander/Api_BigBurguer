from typing import Any

from app.infra.db import Session
from app.order.model import OrderModel


def get(session: Session, order_id: int) -> OrderModel:
    return session.query(OrderModel).filter(OrderModel.id == order_id).one()

def get_all(session: Session, **kwargs: Any) -> list[OrderModel]:
    return session.query(OrderModel).filter_by(**kwargs).all()

def delete(session: Session, order_id: int) -> None:
    m = get(session=session, order_id=order_id)
    return session.delete(m)

def create(session: Session, order: OrderModel) -> OrderModel:
    session.add(order)
    session.flush()
    return order
    
def update(session: Session, order_id: int, **kwargs: Any) -> OrderModel:
    m = get(session=session, order_id=order_id)
    for k, v in kwargs.items():
        setattr(m, k, v)
    return m

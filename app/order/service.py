from typing import Any

from app.infra.db import Session
from app.order import repository
from app.order.model import OrderModel
from app.order.schema import OrderCreateSchema, OrderSchema, OrderUpdateSchema


def get_order(session: Session, order_id: int) -> OrderSchema | None:
    try:
        order = repository.get(order_id=order_id, session=session)
        return OrderSchema(**order.__dict__)
    except BaseException:
        return None


def get_orders(session: Session, **kwargs: Any) -> list[OrderSchema]:
    orders = repository.get_all(session=session, **kwargs)
    return [OrderSchema(**p.__dict__) for p in orders]


def remove_order(session: Session, order_id: int) -> bool:
    with session.begin():
        repository.delete(order_id=order_id, session=session)
    return True


def save_order(session: Session, order: OrderCreateSchema) -> OrderSchema:
    with session.begin():
        order_created = repository.create(session=session, order=OrderModel(**order.__dict__))
        order_ = OrderSchema(**order_created.__dict__)
    return order_


def update_order(
    session: Session, order_id: int, order: OrderUpdateSchema | OrderCreateSchema
) -> OrderSchema:
    with session.begin():
        order_updated = repository.update(session=session, order_id=order_id, **order.model_dump(exclude_none=True))
        order_ = OrderSchema(**order_updated.__dict__)
    return order_

from typing import Any

from app.category.model import CategoryModel
from app.infra.db import Session


def get(session: Session, category_id: int) -> CategoryModel:
    return session.query(CategoryModel).filter(CategoryModel.id == category_id).one()

def get_all(session: Session, **kwargs: Any) -> list[CategoryModel]:
    return session.query(CategoryModel).filter_by(**kwargs).all()

def delete(session: Session, category_id: int) -> None:
    m = get(session=session, category_id=category_id)
    return session.delete(m)

def create(session: Session, category: CategoryModel) -> CategoryModel:
    session.add(category)
    session.flush()
    return category
    
def update(session: Session, category_id: int, **kwargs: Any) -> CategoryModel:
    m = get(session=session, category_id=category_id)
    for k, v in kwargs.items():
        setattr(m, k, v)
    return m

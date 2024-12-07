from typing import Any

from app.category import repository
from app.category.model import CategoryModel
from app.category.schema import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.infra.db import Session


def get_category(session: Session, category_id: int) -> CategorySchema | None:
    try:
        category = repository.get(category_id=category_id, session=session)
        return CategorySchema(**category.__dict__)
    except BaseException:
        return None


def get_categories(session: Session, **kwargs: Any) -> list[CategorySchema]:
    categories = repository.get_all(session=session, **kwargs)
    return [CategorySchema(**p.__dict__) for p in categories]


def remove_category(session: Session, category_id: int) -> bool:
    with session.begin():
        repository.delete(category_id=category_id, session=session)
    return True


def save_category(session: Session, category: CategoryCreateSchema) -> CategorySchema:
    with session.begin():
        category_created = repository.create(session=session, category=CategoryModel(**category.__dict__))
        category_ = CategorySchema(**category_created.__dict__)
    return category_


def update_category(
    session: Session, category_id: int, category: CategoryUpdateSchema | CategoryCreateSchema
) -> CategorySchema:
    with session.begin():
        category_updated = repository.update(session=session, category_id=category_id, **category.model_dump(exclude_none=True))
        category_ = CategorySchema(**category_updated.__dict__)
    return category_

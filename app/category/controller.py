from typing import List

from fastapi import APIRouter, Depends, Response, status

from app.category import service as category_service
from app.category.schema import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.common.response import ResponseOK
from app.infra.db import Session, get_session

app = APIRouter(prefix="/categories", tags=["Category"])


@app.get(
    "/v1/categories",
    response_model=ResponseOK[List[CategorySchema]],
    response_model_exclude_unset=True,
)
def get_all_categories(response: Response, session: Session = Depends(get_session)):
    result = category_service.get_categories(session=session)
    if not result:
        response.status_code = status.HTTP_204_NO_CONTENT
    return ResponseOK(data=result)


@app.post(
    "/v1/categories",
    response_model=ResponseOK[CategorySchema],
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    body: CategoryCreateSchema,
    session: Session = Depends(get_session),
):
    result = category_service.save_category(session=session, category=body)
    return ResponseOK(data=result)


@app.get(
    "/v1/categories/{category_id}",
    response_model=ResponseOK[CategorySchema],
    response_model_exclude_unset=True,
)
def get_category(
    category_id: int, response: Response, session: Session = Depends(get_session)
):
    result = category_service.get_category(session=session, category_id=category_id)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    return ResponseOK(data=result)


@app.delete(
    "/v1/categories/{category_id}",
    response_model=ResponseOK[CategorySchema],
    response_model_exclude_unset=True,
)
def delete_category(category_id: int, session: Session = Depends(get_session)):
    result = category_service.remove_category(session=session, category_id=category_id)
    return ResponseOK(data=result)


@app.patch(
    "/v1/categories/{category_id}",
    response_model=ResponseOK[CategorySchema],
    response_model_exclude_unset=True,
)
def update_category_with_optional_fields(
    category_id: int, body: CategoryUpdateSchema, session: Session = Depends(get_session)
):
    result = category_service.update_category(
        session=session, category_id=category_id, category=body
    )
    return ResponseOK(data=result)


@app.put(
    "/v1/categories/{category_id}",
    response_model=ResponseOK[CategorySchema],
    response_model_exclude_unset=True,
)
def update_category(
    category_id: int, body: CategoryCreateSchema, session: Session = Depends(get_session)
):
    result = category_service.update_category(
        session=session, category_id=category_id, category=body
    )
    return ResponseOK(data=result)

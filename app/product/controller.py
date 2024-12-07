from typing import List

from fastapi import APIRouter, Depends, Response, status

from app.common.response import ResponseOK
from app.infra.db import Session, get_session
from app.product import service as product_service
from app.product.schema import ProductCreateSchema, ProductSchema, ProductUpdateSchema

app = APIRouter(prefix="/products", tags=["Product"])


@app.get(
    "/v1/products",
    response_model=ResponseOK[List[ProductSchema]],
    response_model_exclude_unset=True,
)
def get_all_products(response: Response, session: Session = Depends(get_session)):
    result = product_service.get_products(session=session)
    if not result:
        response.status_code = status.HTTP_204_NO_CONTENT
    return ResponseOK(data=result)


@app.post(
    "/v1/products",
    response_model=ResponseOK[ProductSchema],
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    body: ProductCreateSchema,
    session: Session = Depends(get_session),
):
    result = product_service.save_product(session=session, product=body)
    return ResponseOK(data=result)


@app.get(
    "/v1/products/{product_id}",
    response_model=ResponseOK[ProductSchema],
    response_model_exclude_unset=True,
)
def get_product(
    product_id: int, response: Response, session: Session = Depends(get_session)
):
    result = product_service.get_product(session=session, product_id=product_id)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    return ResponseOK(data=result)


@app.delete(
    "/v1/products/{product_id}",
    response_model=ResponseOK[ProductSchema],
    response_model_exclude_unset=True,
)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    result = product_service.remove_product(session=session, product_id=product_id)
    return ResponseOK(data=result)


@app.patch(
    "/v1/products/{product_id}",
    response_model=ResponseOK[ProductSchema],
    response_model_exclude_unset=True,
)
def update_product_with_optional_fields(
    product_id: int, body: ProductUpdateSchema, session: Session = Depends(get_session)
):
    result = product_service.update_product(
        session=session, product_id=product_id, product=body
    )
    return ResponseOK(data=result)


@app.put(
    "/v1/products/{product_id}",
    response_model=ResponseOK[ProductSchema],
    response_model_exclude_unset=True,
)
def update_product(
    product_id: int, body: ProductCreateSchema, session: Session = Depends(get_session)
):
    result = product_service.update_product(
        session=session, product_id=product_id, product=body
    )
    return ResponseOK(data=result)

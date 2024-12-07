from typing import List

from fastapi import APIRouter, Depends, Response, status

from app.common.response import ResponseOK
from app.infra.db import Session, get_session
from app.order import service as order_service
from app.order.schema import OrderCreateSchema, OrderSchema, OrderUpdateSchema

app = APIRouter(prefix="/orders", tags=["Order"])


@app.get(
    "/v1/orders",
    response_model=ResponseOK[List[OrderSchema]],
    response_model_exclude_unset=True,
)
def get_all_orders(response: Response, session: Session = Depends(get_session)):
    result = order_service.get_orders(session=session)
    if not result:
        response.status_code = status.HTTP_204_NO_CONTENT
    return ResponseOK(data=result)


@app.post(
    "/v1/orders",
    response_model=ResponseOK[OrderSchema],
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    body: OrderCreateSchema,
    session: Session = Depends(get_session),
):
    result = order_service.save_order(session=session, order=body)
    return ResponseOK(data=result)


@app.get(
    "/v1/orders/{order_id}",
    response_model=ResponseOK[OrderSchema],
    response_model_exclude_unset=True,
)
def get_order(
    order_id: int, response: Response, session: Session = Depends(get_session)
):
    result = order_service.get_order(session=session, order_id=order_id)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    return ResponseOK(data=result)


@app.delete(
    "/v1/orders/{order_id}",
    response_model=ResponseOK[OrderSchema],
    response_model_exclude_unset=True,
)
def delete_order(order_id: int, session: Session = Depends(get_session)):
    result = order_service.remove_order(session=session, order_id=order_id)
    return ResponseOK(data=result)


@app.patch(
    "/v1/orders/{order_id}",
    response_model=ResponseOK[OrderSchema],
    response_model_exclude_unset=True,
)
def update_order_with_optional_fields(
    order_id: int, body: OrderUpdateSchema, session: Session = Depends(get_session)
):
    result = order_service.update_order(
        session=session, order_id=order_id, order=body
    )
    return ResponseOK(data=result)


@app.put(
    "/v1/orders/{order_id}",
    response_model=ResponseOK[OrderSchema],
    response_model_exclude_unset=True,
)
def update_order(
    order_id: int, body: OrderCreateSchema, session: Session = Depends(get_session)
):
    result = order_service.update_order(
        session=session, order_id=order_id, order=body
    )
    return ResponseOK(data=result)

from datetime import datetime

from app.common.schema import AllOptionalMetaclass, BaseSchema
from app.order.enum import StatusEnum


class OrderCreateSchema(BaseSchema):
    table: str
    status: StatusEnum
    # employee_id: int


class OrderUpdateSchema(OrderCreateSchema, metaclass=AllOptionalMetaclass):
    ...
    

class OrderSchema(OrderCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

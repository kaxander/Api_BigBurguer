from datetime import datetime
from decimal import Decimal

from app.common.schema import AllOptionalMetaclass, BaseSchema


class ProductCreateSchema(BaseSchema):
    name: str
    description: str
    image: str
    price: Decimal


class ProductUpdateSchema(ProductCreateSchema, metaclass=AllOptionalMetaclass):
    ...
    

class ProductSchema(ProductCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

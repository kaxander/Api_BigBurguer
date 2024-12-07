from datetime import datetime

from app.common.schema import AllOptionalMetaclass, BaseSchema


class ProductCreateSchema(BaseSchema):
    name: str
    description: str
    image: str
    price: str


class ProductUpdateSchema(ProductCreateSchema, metaclass=AllOptionalMetaclass):
    ...
    

class ProductSchema(ProductCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

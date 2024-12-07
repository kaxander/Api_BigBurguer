from datetime import datetime

from app.common.schema import AllOptionalMetaclass, BaseSchema


class CategoryCreateSchema(BaseSchema):
    name: str


class CategoryUpdateSchema(CategoryCreateSchema, metaclass=AllOptionalMetaclass):
    ...
    

class CategorySchema(CategoryCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

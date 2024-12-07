from datetime import datetime

from pydantic import EmailStr

from app.common.schema import AllOptionalMetaclass, BaseSchema

# from pydantic import EmailStr, SecretStr
# from pydantic_extra_types.phone_numbers import PhoneNumber


class EmployeeCreateSchema(BaseSchema):
    name: str
    email: EmailStr
    password: str
    phone_number: str


class EmployeeUpdateSchema(EmployeeCreateSchema, metaclass=AllOptionalMetaclass): ...


class EmployeeSchema(EmployeeCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime

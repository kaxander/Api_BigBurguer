from typing import Generic, TypeVar

from .schema import BaseSchema

T = TypeVar("T")


class ResponseOK(BaseSchema, Generic[T]):
    data: T



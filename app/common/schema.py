from __future__ import annotations

from typing import Any, Optional, Type, TypeVar

from pydantic import AliasGenerator as PydanticAliasGenerator
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict as PydanticConfigDict
from pydantic._internal._model_construction import (
    ModelMetaclass as PydanticModelMetaclass,
)
from pydantic.alias_generators import to_camel as PydanticToCamel

T = TypeVar("T")


class BaseSchema(PydanticBaseModel):
    model_config = PydanticConfigDict(
        alias_generator=PydanticAliasGenerator(
            validation_alias=PydanticToCamel, serialization_alias=PydanticToCamel
        ),
        populate_by_name=True,
    )



class AllOptionalMetaclass(PydanticModelMetaclass):
    def __new__(
        cls: Type[AllOptionalMetaclass],
        name: str,
        bases: tuple[type[Any], ...],
        namespaces: dict[str, Any],
        **kwargs: Any,
    ):
        annotations: dict[str, Any] = namespaces.get("__annotations__", {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = Optional[annotations[field]]
                namespaces[field] = None
        namespaces["__annotations__"] = annotations
        return super().__new__(cls, name, bases, namespaces, **kwargs)




from datetime import datetime

from sqlalchemy import (
    func,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.common.util import to_snakecase


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return to_snakecase(cls.__name__).replace("_model", "")

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
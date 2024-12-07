from decimal import Decimal

from sqlalchemy import (
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db import Base


class ProductModel(Base):
    
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    description: Mapped[str] = mapped_column(String(40), nullable=False)
    image: Mapped[str] = mapped_column(String(40), nullable=False)
    price: Mapped[Decimal] = mapped_column(nullable=False)

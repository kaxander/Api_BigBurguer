from sqlalchemy import (
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db import Base


class CategoryModel(Base):
    __tablename__ = "category"
    
    name: Mapped[str] = mapped_column(String(40), nullable=False)
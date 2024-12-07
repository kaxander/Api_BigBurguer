from sqlalchemy import (
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db import Base


class EmployeeModel(Base):

    name: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(40), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)

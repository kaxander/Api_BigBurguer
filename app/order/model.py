
from sqlalchemy import (
    # ForeignKey,
    String,
)

# from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import Mapped, mapped_column

# from app.employee.model import EmployeeModel
from app.infra.db import Base
from app.order.enum import StatusEnum


class OrderModel(Base):
    
    table: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(nullable=False)
    # employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    
    # employee: Mapped[EmployeeModel] = relationship(back_populates="orders")

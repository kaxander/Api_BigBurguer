from typing import Any

from app.employee.model import EmployeeModel
from app.infra.db import Session


def get(session: Session, employee_id: int) -> EmployeeModel:
    return session.query(EmployeeModel).filter(EmployeeModel.id == employee_id).one()

def get_all(session: Session, **kwargs: Any) -> list[EmployeeModel]:
    return session.query(EmployeeModel).filter_by(**kwargs).all()

def delete(session: Session, employee_id: int) -> None:
    m = get(session=session, employee_id=employee_id)
    return session.delete(m)

def create(session: Session, employee: EmployeeModel) -> EmployeeModel:
    session.add(employee)
    session.flush()
    return employee
    
def update(session: Session, employee_id: int, **kwargs: Any) -> EmployeeModel:
    m = get(session=session, employee_id=employee_id)
    for k, v in kwargs.items():
        setattr(m, k, v)
    return m

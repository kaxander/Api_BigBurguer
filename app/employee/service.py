from typing import Any

from app.employee import repository
from app.employee.model import EmployeeModel
from app.employee.schema import (
    EmployeeCreateSchema,
    EmployeeSchema,
    EmployeeUpdateSchema,
)
from app.infra.db import Session


def get_employee(session: Session, employee_id: int) -> EmployeeSchema | None:
    try:
        employee = repository.get(employee_id=employee_id, session=session)
        return EmployeeSchema(**employee.__dict__)
    except BaseException:
        return None


def get_employees(session: Session, **kwargs: Any) -> list[EmployeeSchema]:
    employees = repository.get_all(session=session, **kwargs)
    return [EmployeeSchema(**p.__dict__) for p in employees]


def remove_employee(session: Session, employee_id: int) -> bool:
    with session.begin():
        repository.delete(employee_id=employee_id, session=session)
    return True


def save_employee(session: Session, employee: EmployeeCreateSchema) -> EmployeeSchema:
    with session.begin():
        employee_created = repository.create(session=session, employee=EmployeeModel(**employee.__dict__))
        employee_ = EmployeeSchema(**employee_created.__dict__)
    return employee_


def update_employee(
    session: Session, employee_id: int, employee: EmployeeUpdateSchema | EmployeeCreateSchema
) -> EmployeeSchema:
    with session.begin():
        employee_updated = repository.update(session=session, employee_id=employee_id, **employee.__dict__)
        employee_ = EmployeeSchema(**employee_updated.__dict__)
    return employee_

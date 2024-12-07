from typing import List

from fastapi import APIRouter, Depends, Response, status

from app.common.response import ResponseOK
from app.employee import service as employee_service
from app.employee.schema import (
    EmployeeCreateSchema,
    EmployeeSchema,
    EmployeeUpdateSchema,
)
from app.infra.db import Session, get_session

app = APIRouter(prefix="/employees", tags=["Employee"])


@app.get(
    "/v1/employees",
    response_model=ResponseOK[List[EmployeeSchema]],
    response_model_exclude_unset=True,
)
def get_all_employees(response: Response, session: Session = Depends(get_session)):
    result = employee_service.get_employees(session=session)
    if not result:
        response.status_code = status.HTTP_204_NO_CONTENT
    return ResponseOK(data=result)


@app.post(
    "/v1/employees",
    response_model=ResponseOK[EmployeeSchema],
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    body: EmployeeCreateSchema,
    session: Session = Depends(get_session),
):
    result = employee_service.save_employee(session=session, employee=body)
    return ResponseOK(data=result)


@app.get(
    "/v1/employees/{employee_id}",
    response_model=ResponseOK[EmployeeSchema],
    response_model_exclude_unset=True,
)
def get_employee(
    employee_id: int, response: Response, session: Session = Depends(get_session)
):
    result = employee_service.get_employee(session=session, employee_id=employee_id)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    return ResponseOK(data=result)


@app.delete(
    "/v1/employees/{employee_id}",
    response_model=ResponseOK[EmployeeSchema],
    response_model_exclude_unset=True,
)
def delete_employee(employee_id: int, session: Session = Depends(get_session)):
    result = employee_service.remove_employee(session=session, employee_id=employee_id)
    return ResponseOK(data=result)


@app.patch(
    "/v1/employees/{employee_id}",
    response_model=ResponseOK[EmployeeSchema],
    response_model_exclude_unset=True,
)
def update_employee_with_optional_fields(
    employee_id: int, body: EmployeeUpdateSchema, session: Session = Depends(get_session)
):
    result = employee_service.update_employee(
        session=session, employee_id=employee_id, employee=body
    )
    return ResponseOK(data=result)


@app.put(
    "/v1/employees/{employee_id}",
    response_model=ResponseOK[EmployeeSchema],
    response_model_exclude_unset=True,
)
def update_employee(
    employee_id: int, body: EmployeeCreateSchema, session: Session = Depends(get_session)
):
    result = employee_service.update_employee(
        session=session, employee_id=employee_id, employee=body
    )
    return ResponseOK(data=result)

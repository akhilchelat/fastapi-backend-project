from pydantic import BaseModel
from typing import Optional


class CreateEmployee(BaseModel):
    name: str
    email: str
    department_id: Optional[int] = None
    salary: float
    user_id: int
    created_by: int


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    department_id: Optional[int]
    department_name: Optional[str]
    salary: float
    user_id: int
    created_by: int
    is_active: bool

    class Config:
        from_attributes = True


class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    salary: Optional[float] = None
    department_id: Optional[int] = None
from pydantic import BaseModel
from typing import Optional

class SalaryRankPerDepartmentResponse(BaseModel):
    employee_id: int
    name: str
    department_name: str
    salary: float
    rank: int

    class Config:
        from_attributes = True

class TopNEmployeesInADepartmentResponse(BaseModel):
    name: str
    department_name: str
    salary: float

    class Config:
        from_attributes = True

class AverageSalaryPerDepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    avg_salary: float

    class Config:
        from_attributes = True

class TopEmployeesPerDepartmentResponse(BaseModel):
    department_name: str
    employee_id: int
    name: str
    salary: float

    class Config:
        from_attributes = True

class EmployeeCountPerDepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    employee_count: int

    class Config:
        from_attributes = True

class HighestSalaryPerDepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    max_salary: float

    class Config:
        from_attributes = True

class SalaryDistributionInADepartmentResponse(BaseModel):
    department_name: str
    min_salary: float
    max_salary: float
    avg_salary: float

    class Config:
        from_attributes = True

class EmployeeRankOverallResponse(BaseModel):
    employee_id: int
    name: str
    department_name: str
    salary: float
    rank: int

    class Config:
        from_attributes = True

class EmployeeSalaryAboveDepartmentAverageResponse(BaseModel):
    employee_id: int
    name: str
    salary: float

    class Config:
        from_attributes = True












            









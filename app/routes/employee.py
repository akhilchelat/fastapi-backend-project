from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from services import employee_services
from security.authorization import require_role
from models.users import User
from schemas import employee_schema

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/create_employee", response_model=employee_schema.EmployeeResponse)
def create_employee(
    emp: employee_schema.CreateEmployee,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin","manager"]))):
    
    return employee_services.create_employee(
        db, emp.name, emp.email, emp.salary, emp.department_id, emp.user_id, emp.created_by)


@router.get("/list_all_employees", response_model=list[employee_schema.EmployeeResponse])
def list_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin","manager"]))):

    return employee_services.get_all_employees(db)


@router.get("/{employee_id}", response_model=employee_schema.EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin","manager"]))):

    return employee_services.get_employee_by_id(db, employee_id)


@router.put("/{employee_id}", response_model=employee_schema.EmployeeResponse)
def update_employee(
    emp: employee_schema.UpdateEmployee,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin","manager"]))):

    return employee_services.update_employee(
        db, emp.employee_id, emp.name, emp.email, emp.salary, emp.department_id)


@router.patch("/delete_user/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin","manager"]))):
    
    return employee_services.employee_soft_delete(db, employee_id)
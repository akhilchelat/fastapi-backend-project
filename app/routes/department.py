from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from services import department_service
from security.authorization import require_role
from models.users import User
from schemas import department_schema

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post("/create_department", response_model=department_schema.DepartmentResponse)
def create_department(
    department: department_schema.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))):
    
    return department_service.create_new_department(db, department.name)


@router.get("/all_department_list", response_model=list[department_schema.DepartmentResponse])
def all_department_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin","manager","employee"]))):

    return department_service.get_all_departments(db)


@router.get("/{department_id}", response_model=department_schema.DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin","manager","employee"]))):

    return department_service.get_department_by_id(db, department_id)


@router.put("/{department_id}", response_model=department_schema.DepartmentResponse)
def update_department(
    department_id: int,
    department: department_schema.DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))):

    return department_service.update_department(db, department_id, department.name)


@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))):
    
    return department_service.delete_department(db, department_id)
from sqlalchemy.orm import Session
from app.models.employees import Employee
from app.models.departments import Department
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import Optional

def create_employee(db: Session, name: str, 
                    email: str, salary: 
                    float, department_id: Optional[int],
                    user_id: int,
                    created_by: int):
    
    name = name.strip()
    email = email.strip()
    
    if department_id is not None:
        existing_department = (db.query(Department)
                .filter(Department.id == department_id, Department.is_active.is_(True)).first())
        
        if not existing_department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    existing_employee =(db.query(Employee)
                        .filter(Employee.email == email).first())
    
    if existing_employee and not existing_employee.is_active:

        existing_employee.name = name
        existing_employee.email = email
        existing_employee.salary = salary
        existing_employee.department_id = department_id
        existing_employee.user_id = user_id
        existing_employee.created_by = created_by
        existing_employee.is_active = True

        db.commit()
        db.refresh(existing_employee)
        return existing_employee
    
    if existing_employee and existing_employee.is_active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already exist")
    
    if not existing_employee:

        new_employee = Employee(name=name, 
                                email=email, 
                                department_id=department_id, 
                                salary=salary,
                                user_id=user_id,
                                created_by=created_by)

        db.add(new_employee)
        try:
            db.commit()
            db.refresh(new_employee)
            return new_employee
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Employee already exists")

def get_employee_by_id(db: Session, employee_id: int):

    employee = (db.query(Employee).filter(Employee.id == employee_id, Employee.is_active.is_(True)).first())

    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    return employee

        
def get_all_employees(db: Session):

    all_employees = (db.query(Employee.id, 
                              Employee.name, 
                              Employee.department_id, 
                              Department.name.label("department_name"),
                              Employee.salary,
                              Employee.is_active,
                              Employee.created_by).join(Employee.department)
                              .filter(Employee.is_active.is_(True))
                              .order_by(Employee.id.desc()).all())  

    return all_employees 
    
def update_employee(db: Session,
                    employee_id: int, 
                    name: Optional[str] = None,
                    email: Optional[str] = None,
                    salary: Optional[float] = None,
                    department_id: Optional[int] = None):
    
    employee = (db.query(Employee).filter(Employee.id == employee_id, Employee.is_active.is_(True)).first())

    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if name is not None:
        employee.name = name.strip()

    if email is not None:

        existing_email = (db.query(Employee).filter(Employee.email == email, Employee.id != employee_id).first())     

        if existing_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")  
        
        employee.email = email.strip()

    if salary is not None:
        employee.salary = salary

    if department_id is not None:
        
        existing_department = (db.query(Department).filter(Department.id == department_id, Department.is_active.is_(True)).first()) 

        if not existing_department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

        employee.department_id = department_id

    db.commit()
    db.refresh(employee)

    return employee    

def employee_soft_delete(db: Session, employee_id: int):

    employee = (db.query(Employee).filter(Employee.id == employee_id, Employee.is_active.is_(True)).first())

    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    employee.is_active = False
    db.commit()

    return {"message": "Employee deleted successfully"}   

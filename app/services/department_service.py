from sqlalchemy.orm import Session
from models.departments import Department
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

def create_new_department(db: Session, department_name: str):

    department_name = department_name.strip()
    
    existing_department = (db.query(Department).filter(Department.name == department_name, Department.is_active.is_(True)).first())

    if existing_department:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already exist")
    
    new_department = Department(name=department_name)
    db.add(new_department)     
    try:
        db.commit()
        db.refresh(new_department)
        return new_department
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department already exists")

def get_department_by_id(db: Session, department_id: int):

    existing_department = (db.query(Department).filter(Department.id == department_id, Department.is_active.is_(True)).first())

    if not existing_department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return existing_department  

def get_all_departments(db: Session):

    all_departments = (db.query(Department).filter(Department.is_active.is_(True)).all())

    return all_departments

def update_department(db: Session, department_id: int, department_name: str):

    department_name = department_name.strip()

    existing_department = (db.query(Department).filter(Department.id == department_id, Department.is_active.is_(True)).first())

    if not existing_department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    existing_department.name = department_name

    db.commit()
    db.refresh(existing_department)

    return existing_department

def delete_department(db: Session, department_id: int):

    existing_department = (db.query(Department).filter(Department.id == department_id, Department.is_active.is_(True)).first())

    if not existing_department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    existing_department.is_active = False

    db.commit()



    
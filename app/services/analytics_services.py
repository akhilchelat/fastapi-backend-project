from sqlalchemy.orm import Session
from sqlalchemy import func
from models.employees import Employee
from models.departments import Department
from fastapi import status, HTTPException

def salary_ranking_per_department(db: Session, department_id: int):

    dep = (db.query(Department).filter(Department.id == department_id, Department.is_active.is_(True)).first())

    if not dep:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    salary_ranking = (db.query(Employee.id.label("employee_id"),
                               Employee.name.label("name"),     
                               Department.name.label("department_name"),
                               Employee.salary.label("salary"),
                               func.rank().over(partition_by=Employee.department_id, order_by=Employee.salary.desc()).label("rank"))
                               .join(Employee.department)
                               .filter(Employee.department_id == department_id, Employee.is_active.is_(True)).all())
    
    return salary_ranking

def top_n_employees_in_a_department(db: Session, department_id: int, limit: int):

    department = (db.query(Department).filter(Department.id == department_id, Department.is_active.is_(True)).first())

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    top_n_in_the_department = (db.query(Employee.name.label("name"),
                                Department.name.label("department_name"),
                                Employee.salary.label("salary"))
                                .join(Employee.department)
                                .filter(Employee.department_id == department_id, Employee.is_active.is_(True))
                                .order_by(Employee.salary.desc())
                                .limit(limit).all())
    
    return top_n_in_the_department

def average_salary_per_department(db: Session):

    avg_salary = func.avg(Employee.salary).label("avg_salary")

    avg_salary_per_department = (db.query(Department.id.label("department_id"),
                                          Department.name.label("department_name"),
                                          avg_salary)
                                          .join(Department.employees)
                                          .filter(Employee.is_active.is_(True), Department.is_active.is_(True))
                                          .group_by(Department.id, Department.name)
                                          .order_by(avg_salary.desc())
                                          .all())
    
    return avg_salary_per_department

def top_employees_per_department(db: Session):

    sub = (db.query(Department.name.label("department_name"),
                       Employee.id.label("employee_id"),
                       Employee.name.label("name"),
                       Employee.salary.label("salary"),
                       func.rank().over(partition_by=Employee.department_id, order_by=Employee.salary.desc()).label("rank"))
                       .join(Employee.department)
                       .filter(Employee.is_active.is_(True), Department.is_active.is_(True))
                       .subquery())
    
    result = (db.query(sub.c.department_name, sub.c.employee_id, sub.c.name,
                       sub.c.salary)
                       .filter(sub.c.rank == 1)
                       .order_by(sub.c.department_name)
                       .all())
    
    return result

def employee_count_per_department(db: Session):
    
    sub  = (db.query(Department.id.label("department_id"),
                       Department.name.label("department_name"),
                       func.count(Employee.id).label("employee_count"))
                       .join(Department.employees)
                       .filter(Employee.is_active.is_(True), Department.is_active.is_(True))
                       .group_by(Department.id, Department.name).subquery())
    
    emp_count_per_department = (db.query(sub.c.department_id,
                                         sub.c.department_name,
                                         sub.c.employee_count)
                                         .order_by(sub.c.employee_count.desc()).all())
    
    
    return emp_count_per_department

def highest_salary_per_department(db: Session):

    sub = (db.query(Department.id.label("department_id"),
                    Department.name.label("department_name"),
                    func.max(Employee.salary).label("max_salary"))
                    .join(Department.employees)
                    .filter(Employee.is_active.is_(True), Department.is_active.is_(True))
                    .group_by(Department.id, Department.name)
                    .subquery())
    
    highest_salary_per_dep = (db.query(sub.c.department_id,
                                       sub.c.department_name,
                                       sub.c.max_salary)
                                       .order_by(sub.c.max_salary.desc()).all())
    
    return highest_salary_per_dep

def salary_distribution_in_a_department(db: Session, department_id: int):

    department = (db.query(Department).filter(Department.id == department_id, Department.is_active.is_(True)).first())

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    salary_analytics = (db.query(Department.name.label("department_name"),
                       func.min(Employee.salary).label("min_salary"),
                       func.max(Employee.salary).label("max_salary"),
                       func.avg(Employee.salary).label("avg_salary"))
                       .join(Employee.department)
                       .filter(Employee.is_active.is_(True), Department.is_active.is_(True), Department.id == department_id)
                       .group_by(Department.name).all())
    
    return salary_analytics

def employee_rank_overall(db: Session):

    employee_global_ranking = (db.query(Employee.id.label("employee_id"),
                                        Employee.name.label("name"),
                                        Department.name.label("department_name"),
                                        Employee.salary.label("salary"),
                                        func.rank().over(order_by=(Employee.salary.desc(), Employee.id)).label("rank"))
                                        .join(Employee.department)
                                        .filter(Employee.is_active.is_(True), Department.is_active.is_(True))
                                        .all())

    return employee_global_ranking

def employee_salary_above_department_average(db: Session, department_id: int):

    department = (db.query(Department).filter(Department.id == department_id, Department.is_active.is_(True)).first())

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    sub = (db.query(Employee.id.label("employee_id"),
                    Employee.name.label("name"),
                    Employee.salary.label("salary"),
                    func.avg(Employee.salary).over(partition_by=Employee.department_id).label("avg_dep_salary"))
                    .join(Employee.department)
                    .filter(Employee.is_active.is_(True), Department.is_active.is_(True), Department.id == department_id)
                    .subquery())

    employee_salary_above_dep_avg = (db.query(sub.c.employee_id,
                                              sub.c.name,
                                              sub.c.salary)
                                              .filter(sub.c.salary > sub.c.avg_dep_salary)
                                              .order_by(sub.c.salary.desc()).all())

    return employee_salary_above_dep_avg    

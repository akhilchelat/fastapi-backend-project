from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import analytics_services
from app.security.authorization import require_role
from app.models.users import User
from app.schemas import analytics_schema

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/department/{department_id}/salary-ranking", response_model=list[analytics_schema.SalaryRankPerDepartmentResponse])
def salary_ranking(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))):
    
    return analytics_services.salary_ranking_per_department(db, department_id)


@router.get("/department/{department_id}/top/{limit}", response_model=list[analytics_schema.TopNEmployeesInADepartmentResponse])
def top_n_employees(
    department_id: int,
    limit: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))):
 
    return analytics_services.top_n_employees_in_a_department(db, department_id, limit)


@router.get("/average_salary_per_department", response_model=list[analytics_schema.AverageSalaryPerDepartmentResponse])
def avg_salary_per_department(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))):
    
    return analytics_services.average_salary_per_department(db)


@router.get("/top_emp_per_department", response_model=list[analytics_schema.TopEmployeesPerDepartmentResponse])
def top_emp_per_department(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))):
    
    return analytics_services.top_employees_per_department(db)

@router.get("/emp_count_per_department", response_model=list[analytics_schema.EmployeeCountPerDepartmentResponse])
def emp_count_per_department(db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))):

    return analytics_services.employee_count_per_department(db)

@router.get("/high_salary_per_department", response_model=list[analytics_schema.HighestSalaryPerDepartmentResponse])
def high_salary_per_department(db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))):

    return analytics_services.highest_salary_per_department(db)

@router.get("/department/{department_id}/salary_distribution", response_model=list[analytics_schema.SalaryDistributionInADepartmentResponse])
def salary_distribution_per_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))):

    return analytics_services.salary_distribution_in_a_department(db, department_id)

@router.get("/employee_global_salary_rank", response_model=list[analytics_schema.EmployeeRankOverallResponse])
def employee_global_salary_rank(db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))):

    return analytics_services.employee_rank_overall(db)

@router.get("/department/{department_id}/emp_salary_above_dept_avg", response_model=list[analytics_schema.EmployeeSalaryAboveDepartmentAverageResponse])
def emp_salary_above_dept_avg(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))):

    return analytics_services.employee_salary_above_department_average(db, department_id)


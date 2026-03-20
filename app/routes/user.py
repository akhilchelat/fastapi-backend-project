from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from services import user_services
from security.authorization import require_role
from security.authentication import get_current_user
from models.users import User
from schemas import user_schema


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login", response_model=user_schema.TokenResponse)
def login(
    user: user_schema.UserLogin,
    db: Session = Depends(get_db)):

    return user_services.user_login(db, user.email, user.password)


@router.post("/create_user", response_model=user_schema.UserResponse)
def create_user(
    user: user_schema.CreateUser,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin","manager"]))):

    return user_services.create_user(db, user.name, user.email, user.password, user.role, current_user)

 
@router.get("/list_all_users", response_model=list[user_schema.UserResponse])
def list_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin","manager"]))):

    return user_services.list_users(db, current_user)


@router.get("/get_user/{user_id}", response_model=user_schema.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    return user_services.get_user(db, user_id, current_user)


@router.delete("/delete_user/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin","manager"]))):
    
    return user_services.user_soft_delete(db, user_id, current_user)
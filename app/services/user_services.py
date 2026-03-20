from models.users import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from typing import Optional
from security.hashing import hash_password, verify_password
from sqlalchemy.exc import IntegrityError
from security.authorization import require_role
from security.authentication import create_access_token

def create_user(db: Session, name: str, email: str, password: str, role: str, current_user: User):

    name = name.strip()
    email = email.strip()
    password = password.strip()
    role = role.strip().lower()

    allowed_roles = ["admin", "manager", "employee"]

    if role not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")

    if current_user.role == "employee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create users")
    
    if current_user.role == "manager" and role != "employee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create users")

    existing_user = (db.query(User).filter(User.email == email).first())

    if existing_user and not existing_user.is_active:

        existing_user.is_active = True
        
        db.commit()
        db.refresh(existing_user)
        return existing_user
    
    if existing_user and existing_user.is_active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already exist")
    
    hashed_password = hash_password(password)
    
    new_user = User(name=name, email=email, hashed_password=hashed_password, role=role)

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already exist")

def update_user(db: Session, current_user: User,
                user_id: int, name: Optional[str] = None, 
                email: Optional[str] = None, 
                role: Optional[str] = None):
    
    user = (db.query(User).filter(User.id == user_id, User.is_active.is_(True)).first())

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")  
            
    if current_user.role == "employee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create users")
    
    allowed_roles = ["admin", "manager", "employee"]

    if role is not None:
        role = role.strip().lower()
        if role not in allowed_roles:
            raise HTTPException(status_code=400, detail="Invalid role")
    
    if current_user.role == "manager":
        if user.role != "employee":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager can create employee only")
        
        if role and role.lower() != "employee":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager can't change roles")
           
    if name is not None:
        user.name = name.strip()

    if email is not None:

        email = email.strip()
        
        existing_email = (db.query(User).filter(User.email == email, User.id != user.id, User.is_active.is_(True)).first()) 
        
        if existing_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exist") 

        user.email = email

    if role is not None:
        user.role = role.strip().lower()

    db.commit()
    db.refresh(user)

    return user        

def user_soft_delete(db: Session, user_id: int, current_user: User):

    user = (db.query(User).filter(User.id == user_id, User.is_active.is_(True)).first())

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    if current_user.role == "employee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Employee can't delete user")
    
    if current_user.role == "manager" and user.role != "employee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager can delete only employees") 
    
    if user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin can't be deleted")
    
    user.is_active = False
    db.commit()
    db.refresh(user)

    return {"message": "User deleted successfully"}

def get_user(db: Session, user_id: int, current_user: User):

    user = (db.query(User).filter(User.id == user_id, User.is_active.is_(True)).first())

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    if current_user.role == "employee":
        if current_user.id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Employee can't see other user data")

    if current_user.role == "manager" and user.role != "employee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager can see only employees") 

    return user

def list_users(db: Session, current_user: User):

    if current_user.role == "employee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access deniel")
    
    if current_user.role == "manager":
        return (db.query(User.id, 
                      User.name,
                      User.email,
                      User.role,
                      User.is_active).filter(User.role == "employee", User.is_active.is_(True)).order_by(User.id.asc()).all())
    
    users = (db.query(User.id, 
                      User.name,
                      User.email,
                      User.role,
                      User.is_active).filter(User.is_active.is_(True)).order_by(User.id.asc()).all())
   
    return users

def user_password_change(db: Session, old_password: str, new_password: str, current_user: User):

    user = (db.query(User).filter(User.id == current_user.id, User.is_active.is_(True)).first())

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    if not verify_password(old_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid password")
    
    changed_password = hash_password(new_password)

    if verify_password(new_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password cannot be same as old password")
    
    user.hashed_password = changed_password
    db.commit()

    return {"message": "password changed successfully"}

def reset_user_password(db: Session, user_id: int, new_password: str, current_user: User):

    user = (db.query(User).filter(User.id == user_id, User.is_active.is_(True)).first())

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    if current_user.role == "employee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Employee can't reset password")
    
    if current_user.role == "manager" and user.role != "employee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager can reset only employee password")
    
    if user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cant reset admin password")
    
    if verify_password(new_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password cannot be same as old password")
    
    user.hashed_password = hash_password(new_password)
    db.commit() 

    return {"message": "password changed successfully"}

def user_login(db: Session, email: str, password: str):

    user = (db.query(User).filter(User.email == email, User.is_active.is_(True)).first())

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credential")
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credential")
    
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})

    return {"access_token": access_token,
            "token_type": "bearer"}


    
    



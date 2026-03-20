from app.security.authentication import get_current_user
from app.models.users import User
from fastapi import HTTPException, status, Depends

def require_role(required_roles: list):

    def role_checker(current_user: User = Depends(get_current_user)):

        if current_user.role not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        
        return current_user

    return role_checker

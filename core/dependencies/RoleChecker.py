from typing import Any, List

from fastapi import Depends, HTTPException, status

from core.dependencies.auth import auth
from user.models.user import User, UserRole


class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(auth.get_current_user)) -> Any:

        if not user.role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User has no role assigned!",
            )
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action!",
            )
        return True

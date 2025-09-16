from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from auth import get_current_user
from db import engine
from models import User as UserModel


class AuthMiddleware:
    """Middleware for handling authentication and authorization."""

    @staticmethod
    async def require_auth(
        current_user: Annotated[UserModel, Depends(get_current_user)]
    ) -> UserModel:
        """Require authentication for a route."""
        return current_user

    @staticmethod
    async def require_user_access(
        user_id: str,
        current_user: Annotated[UserModel, Depends(get_current_user)]
    ) -> UserModel:
        """Require that the current user can access the specified user's data."""
        if current_user.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this user's data"
            )
        return current_user

    @staticmethod
    async def get_user_from_db(user_id: str) -> Optional[UserModel]:
        """Get user from database by user_id."""
        with Session(engine) as session:
            stmt = select(UserModel).where(UserModel.user_id == user_id)
            return session.exec(stmt).first()


async def require_authentication(
    current_user: Annotated[UserModel, Depends(get_current_user)]
) -> UserModel:
    """Dependency to require authentication."""
    return current_user


def require_user_permission(user_id: str):
    """Factory function to create a dependency that checks user permissions."""
    async def check_permission(
        current_user: Annotated[UserModel, Depends(get_current_user)]
    ) -> UserModel:
        if current_user.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this resource"
            )
        return current_user
    return check_permission

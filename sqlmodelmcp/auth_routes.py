from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    UserCreate,
    UserResponse,
    Token,
    authenticate_user,
    create_access_token,
    create_user,
    get_current_active_user,
    get_current_user,
)
from models import User as UserModel

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    """Register a new user."""
    try:
        user = create_user(user_data)
        return UserResponse.from_orm(user)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """Authenticate user and return access token."""
    user = authenticate_user(
        form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)]
):
    """Get current user information."""
    return UserResponse.from_orm(current_user)


@router.get("/protected")
async def protected_route(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    """Example protected route that requires authentication."""
    return {
        "message": f"Hello {current_user.firstname} {current_user.lastname}!",
        "user_id": current_user.user_id,
        "email": current_user.email
    }

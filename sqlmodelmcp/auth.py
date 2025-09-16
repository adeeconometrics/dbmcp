from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from jwt import PyJWTError, encode, decode

from db import engine
from models import User as UserModel

# Configuration
SECRET_KEY = "41a67a70b8cba341d22fb9951fd516459ae0ce9ca1cde0ec3e944b8b2782f6e4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class UserResponse(BaseModel):
    """Pydantic model for user response."""
    user_id: str
    email: str
    firstname: str
    lastname: str
    created_at: datetime

    class Config:
        """Config for ORM mode."""
        from_attributes = True


class UserCreate(BaseModel):
    """Pydantic model for creating a new user."""
    email: EmailStr
    firstname: str
    lastname: str
    password: str
    address_id: Optional[str] = None
    payment_info: Optional[str] = None


class UserLogin(BaseModel):
    """Pydantic model for user login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Pydantic model for JWT token response."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Pydantic model for token data."""
    email: Optional[str] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password for storing in the database."""
    return pwd_context.hash(password)


# Database operations
def get_user_by_email(email: str) -> Optional[UserModel]:
    """Get user by email from database."""
    with Session(engine) as session:
        stmt = select(UserModel).where(UserModel.email == email)
        return session.exec(stmt).first()


def create_user(user_data: UserCreate) -> UserModel:
    """Create a new user in the database."""
    with Session(engine) as session:
        # Check if user already exists
        existing_user = get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = UserModel(
            email=user_data.email,
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            password=hashed_password,
            address_id=user_data.address_id,
            payment_info=user_data.payment_info
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def authenticate_user(email: str, password: str) -> Optional[UserModel]:
    """Authenticate a user by email and password."""
    user = get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


# JWT token operations
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependencies
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserModel:
    """Get the current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except PyJWTError:
        raise credentials_exception

    user = get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
) -> UserModel:
    """Get the current active user (for future use if you add user status)."""
    # You can add a 'disabled' or 'active' field to your User model if needed
    return current_user

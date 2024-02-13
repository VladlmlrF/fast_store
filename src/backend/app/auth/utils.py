from datetime import datetime
from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.backend.app.core.config import settings
from src.backend.app.core.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str | None = None,
        scopes: dict[str, str] | None = None,
        auto_error: bool = True,
    ) -> None:
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        authorization: str = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/login")


def get_password_hash(password: str) -> str:
    """Hash the password"""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Password verification"""
    return pwd_context.verify(password, hashed_password)


def create_access_token(
    payload: dict,
    algorithm: str = settings.algorithm,
    private_key: str = settings.private_key_path.read_text(),
    expires_timedelta: timedelta | None = None,
    expire_minutes: int = settings.access_token_expire_minutes,
) -> str:
    """Encode token"""
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expires_timedelta:
        expire = now + expires_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=private_key, algorithm=algorithm)
    return encoded_jwt


def decode_access_token(
    token: str,
    public_key: str = settings.public_key_path.read_text(),
    algorithm: str = settings.algorithm,
) -> dict:
    """Decode token"""
    decoded = jwt.decode(token=token, key=public_key, algorithms=[algorithm])
    return decoded


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    """Get user by username"""
    try:
        statement = select(User).where(User.username == username)
        user: User | None = await session.scalar(statement=statement)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {username} not found",
            )
        return user
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def authenticate_user(
    session: AsyncSession, username: str = Form(), password: str = Form()
) -> User | None:
    """Checking user authentication"""
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password"
    )
    user = await get_user_by_username(session=session, username=username)
    if not user:
        raise unauthed_exc
    if not verify_password(password=password, hashed_password=user.hashed_password):
        raise unauthed_exc
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user inactive"
        )
    return user


async def get_current_user_name(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    """Get current user name"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict = decode_access_token(token=token)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


async def super_admin_required(
    session: AsyncSession,
    current_user_name: str = Depends(get_current_user_name),
) -> User:
    current_user: User | None = await get_user_by_username(
        session=session, username=current_user_name
    )
    if not current_user or not current_user.is_super_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Super admin access required",
        )
    return current_user


async def admin_required(
    session: AsyncSession,
    current_user_name: str = Depends(get_current_user_name),
) -> User:
    current_user: User | None = await get_user_by_username(
        session=session, username=current_user_name
    )
    if not current_user or (
        not current_user.is_admin and not current_user.is_super_admin
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admin access required",
        )
    return current_user

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..auth.utils import get_password_hash
from ..auth.utils import get_user_by_username
from ..core.config import settings
from ..core.models import User
from ..core.models.user import Role
from .schemas import UserCreateSchema
from .schemas import UserUpdateSchema


async def create_user(session: AsyncSession, user: UserCreateSchema) -> User:
    """Create User"""
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
    )
    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with that username or email already exists!",
        )


async def get_users_by_role(session: AsyncSession, role: Role) -> list[User]:
    """Get user by role"""
    try:
        statement = select(User).where(User.role == role).order_by(User.id)
        result: Result = await session.execute(statement=statement)
        users: list[User] = result.scalars().all()
        return users
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def create_super_admin(session: AsyncSession) -> User | None:
    """Create Super admin if not exists"""
    super_admin_exists = await get_users_by_role(session=session, role=Role.SUPER_ADMIN)
    if super_admin_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Super admin already exists!"
        )

    super_admin = User(
        username="superadmin",
        email="superadmin@example.com",
        hashed_password=get_password_hash(settings.SUPER_ADMIN_PASSWORD),
        role=Role.SUPER_ADMIN,
    )
    try:
        session.add(super_admin)
        await session.commit()
        await session.refresh(super_admin)
        return super_admin
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Creating a super admin is not possible!!",
        )


async def change_admin_rights(
    session: AsyncSession, username: str, make_admin: bool
) -> User:
    """Change admin rights to the user"""
    try:
        user = await get_user_by_username(session=session, username=username)
        if user:
            target_role = Role.ADMIN if make_admin else Role.USER
            if user.role == target_role:
                return user
            user.role = target_role
            await session.commit()
            await session.refresh(user)
            return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {username} not found"
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_users(session: AsyncSession) -> list[User]:
    """Get all users"""
    try:
        statement = select(User).order_by(User.id)
        result: Result = await session.execute(statement=statement)
        users = result.scalars().all()
        return list(users)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    """Get user by user_id"""
    try:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )
        return user
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdateSchema,
) -> User:
    """Update user"""
    if user.role == Role.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN!!!"
        )
    try:
        for name, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, name, value)
        await session.commit()
        await session.refresh(user)
        return user
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_user(session: AsyncSession, user: User) -> None:
    """Delete user"""
    if user.role == Role.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN!!!"
        )
    try:
        await session.delete(user)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def change_user_activity(
    session: AsyncSession,
    username: str,
) -> User:
    """Change user activity"""
    try:
        user = await get_user_by_username(session=session, username=username)
        if user:
            if user.role == Role.SUPER_ADMIN:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN!!!"
                )
            user.is_active = False if user.is_active else True
            await session.commit()
            await session.refresh(user)
            return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {username} not found"
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )

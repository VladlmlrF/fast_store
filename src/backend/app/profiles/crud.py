from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.core.models import Profile
from src.backend.app.profiles.schemas import ProfileCreateSchema
from src.backend.app.profiles.schemas import ProfileUpdateSchema


async def create_profile(
    session: AsyncSession, profile: ProfileCreateSchema
) -> Profile:
    """Create new profile"""
    new_profile = Profile(
        user_id=profile.user_id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        phone_number=profile.phone_number,
    )
    try:
        session.add(new_profile)
        await session.commit()
        await session.refresh(new_profile)
        return new_profile
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_profile(profile_id: int, session: AsyncSession) -> Profile | None:
    """Get profile by id"""
    try:
        statement = select(Profile).where(Profile.id == profile_id)
        profile: Profile | None = await session.scalar(statement=statement)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile {profile_id} not found",
            )
        return profile
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_profiles(session: AsyncSession) -> list[Profile]:
    """Get all profiles"""
    try:
        statement = select(Profile)
        result: Result = await session.execute(statement=statement)
        profiles = result.scalars().all()
        return list(profiles)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def update_profile(
    session: AsyncSession,
    profile: Profile,
    profile_update: ProfileUpdateSchema,
) -> Profile:
    """Update profile"""
    try:
        for name, value in profile_update.model_dump(exclude_unset=True).items():
            setattr(profile, name, value)
        await session.commit()
        await session.refresh(profile)
        return profile
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_profile(session: AsyncSession, profile: Profile) -> None:
    """Delete profile"""
    try:
        await session.delete(profile)
        await session.commit()
        return None
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.auth.utils import admin_required
from src.backend.app.auth.utils import get_current_user_name
from src.backend.app.core.models import db_helper
from src.backend.app.profiles import crud
from src.backend.app.profiles.schemas import ProfileCreateSchema
from src.backend.app.profiles.schemas import ProfileSchema
from src.backend.app.profiles.schemas import ProfileUpdateSchema

router = APIRouter(tags=["Profile"])


@router.post(
    "/",
    response_model=ProfileSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    profile_in: ProfileCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_profile(session=session, profile=profile_in)


@router.get("/", response_model=list[ProfileSchema])
async def get_profiles(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.get_profiles(session=session)


@router.get("/{profile_id}", response_model=ProfileSchema)
async def get_profile(
    profile_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.get_profile(profile_id=profile_id, session=session)


@router.patch("/{profile_id}", response_model=ProfileSchema)
async def update_profile(
    profile_id: int,
    profile_update: ProfileUpdateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    profile = await crud.get_profile(profile_id=profile_id, session=session)
    return await crud.update_profile(
        session=session, profile=profile, profile_update=profile_update
    )


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    profile_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    profile = await crud.get_profile(profile_id=profile_id, session=session)
    await crud.delete_profile(session=session, profile=profile)
    return None

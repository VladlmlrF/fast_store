from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.auth.utils import admin_required
from src.backend.app.auth.utils import get_current_user_name
from src.backend.app.auth.utils import super_admin_required
from src.backend.app.core.models import db_helper
from src.backend.app.users import crud
from src.backend.app.users.schemas import UserCreateSchema
from src.backend.app.users.schemas import UserSchema
from src.backend.app.users.schemas import UserUpdateSchema


router = APIRouter(tags=["User"])


@router.post(
    "/create-super-admin",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_super_admin(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_super_admin(session=session)


@router.post(
    "/activate_admin",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def activate_admin(
    username: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await super_admin_required(session=session, current_user_name=current_user_name)
    return await crud.change_admin_rights(
        session=session, username=username, make_admin=True
    )


@router.post(
    "/deactivate-admin",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def deactivate_admin(
    username: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await super_admin_required(session=session, current_user_name=current_user_name)
    return await crud.change_admin_rights(
        session=session,
        username=username,
        make_admin=False,
    )


@router.post(
    "/",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_in: UserCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(session=session, user=user_in)


@router.get("/", response_model=list[UserSchema])
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.get_users(session=session)


@router.get("/{username}", response_model=UserSchema)
async def get_user(
    username: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    user = await crud.get_user_by_username(session=session, username=username)
    return user


@router.patch("/{username}", response_model=UserSchema)
async def update_user(
    username: str,
    user_update: UserUpdateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    user = await crud.get_user_by_username(session=session, username=username)
    return await crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
    )


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    username: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await super_admin_required(session=session, current_user_name=current_user_name)
    user = await crud.get_user_by_username(session=session, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {username} not found"
        )
    await crud.delete_user(session=session, user=user)
    return None


@router.post("/deactivate_user", response_model=UserSchema)
async def deactivate_user(
    username: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.change_user_activity(session=session, username=username)

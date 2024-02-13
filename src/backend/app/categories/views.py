from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.auth.utils import admin_required
from src.backend.app.auth.utils import get_current_user_name
from src.backend.app.auth.utils import super_admin_required
from src.backend.app.categories import crud
from src.backend.app.categories.schemas import CategoryCreateSchema
from src.backend.app.categories.schemas import CategorySchema
from src.backend.app.categories.schemas import CategoryUpdateSchema
from src.backend.app.core.models import db_helper

router = APIRouter(tags=["Category"])


@router.post(
    "/",
    response_model=CategorySchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category_in: CategoryCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.create_category(session=session, category=category_in)


@router.get("/", response_model=list[CategorySchema])
async def get_categories(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_categories(session=session)


@router.get("/{category_name}", response_model=CategorySchema)
async def get_category_by_name(
    category_name: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_category_by_name(session=session, name=category_name)


@router.patch("/{category_name}", response_model=CategorySchema)
async def update_category(
    category_name: str,
    category_update: CategoryUpdateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    category = await crud.get_category_by_name(session=session, name=category_name)
    return await crud.update_category(
        session=session, category=category, category_update=category_update
    )


@router.delete("/{category_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_name: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await super_admin_required(session=session, current_user_name=current_user_name)
    category = await crud.get_category_by_name(session=session, name=category_name)
    await crud.delete_category(session=session, category=category)
    return None

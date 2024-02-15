from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.auth.utils import admin_required
from src.backend.app.auth.utils import get_current_user_name
from src.backend.app.carts import crud
from src.backend.app.carts.schemas import CartCreateSchema
from src.backend.app.carts.schemas import CartSchema
from src.backend.app.core.models import db_helper

router = APIRouter(tags=["Cart"])


@router.post(
    "/",
    response_model=CartSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_cart(
    cart_in: CartCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_cart(session=session, cart=cart_in)


@router.get("/", response_model=list[CartSchema])
async def get_carts(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.get_carts(session=session)


@router.get("/{cart_id}", response_model=CartSchema)
async def get_cart(
    cart_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.get_cart_by_id(cart_id=cart_id, session=session)


@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(
    cart_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    cart = await crud.get_cart_by_id(cart_id=cart_id, session=session)
    await crud.delete_cart(cart=cart, session=session)
    return None

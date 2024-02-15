from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.auth.utils import admin_required
from src.backend.app.auth.utils import get_current_user_name
from src.backend.app.cart_items import crud
from src.backend.app.cart_items.schemas import CartItemCreateSchema
from src.backend.app.cart_items.schemas import CartItemSchema
from src.backend.app.cart_items.schemas import CartItemUpdateSchema
from src.backend.app.core.models import db_helper

router = APIRouter(tags=["Cart item"])


@router.post(
    "/",
    response_model=CartItemSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_cart_item(
    cart_item_in: CartItemCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_cart_item(session=session, cart_item=cart_item_in)


@router.get("/", response_model=list[CartItemSchema])
async def get_cart_items(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.get_cart_items(session=session)


@router.get("/cart/{cart_id}", response_model=list[CartItemSchema])
async def get_cart_items_by_cart_id(
    cart_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_cart_items_by_cart_id(cart_id=cart_id, session=session)


@router.get("/{cart_item_id}", response_model=CartItemSchema)
async def gey_cart_item(
    cart_item_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_cart_item_by_id(cart_item_id=cart_item_id, session=session)


@router.patch("/{cart_item_id}", response_model=CartItemSchema)
async def update_cart_item(
    cart_item_id: int,
    cart_item_update: CartItemUpdateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    cart_item = await crud.get_cart_item_by_id(
        cart_item_id=cart_item_id, session=session
    )
    return await crud.update_cart_item(
        session=session, cart_item=cart_item, cart_item_update=cart_item_update
    )


@router.delete("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(
    cart_item_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    cart_item = await crud.get_cart_item_by_id(
        cart_item_id=cart_item_id, session=session
    )
    await crud.delete_cart_item(session=session, cart_item=cart_item)

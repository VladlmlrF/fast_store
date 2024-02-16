from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.auth.utils import admin_required
from src.backend.app.auth.utils import get_current_user_name
from src.backend.app.core.models import db_helper
from src.backend.app.orders import crud
from src.backend.app.orders.schemas import OrderCreateSchema
from src.backend.app.orders.schemas import OrderSchema
from src.backend.app.orders.schemas import OrderUpdateSchema

router = APIRouter(tags=["Order"])


@router.post("/", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_order(session=session, order=order_in)


@router.get("/", response_model=list[OrderSchema])
async def get_orders(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.get_orders(session=session)


@router.get("/{order_id}", response_model=OrderSchema)
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_order(order_id=order_id, session=session)


@router.patch("/{order_id}", response_model=OrderSchema)
async def update_order(
    order_id: int,
    order_update: OrderUpdateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    order = await crud.get_order(order_id=order_id, session=session)
    return await crud.update_order(
        session=session, order=order, order_update=order_update
    )


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    order = await crud.get_order(order_id=order_id, session=session)
    await crud.delete_order(session=session, order=order)

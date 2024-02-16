from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.auth.utils import admin_required
from src.backend.app.auth.utils import get_current_user_name
from src.backend.app.core.models import db_helper
from src.backend.app.order_products import crud
from src.backend.app.order_products.schemas import OrderProductCreateSchema
from src.backend.app.order_products.schemas import OrderProductSchema
from src.backend.app.order_products.schemas import OrderProductUpdateSchema

router = APIRouter(tags=["Order Product"])


@router.post(
    "/",
    response_model=OrderProductSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_order_product(
    order_product_in: OrderProductCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_order_product(
        session=session, order_product=order_product_in
    )


@router.get("/", response_model=list[OrderProductSchema])
async def get_order_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.get_order_products(session=session)


@router.get("/{order_id}/{product_id}", response_model=OrderProductSchema)
async def get_order_product(
    order_id: int,
    product_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_order_product(
        order_id=order_id, product_id=product_id, session=session
    )


@router.patch("/{order_id}/{product_id}", response_model=OrderProductSchema)
async def update_order_product(
    order_id: int,
    product_id: int,
    order_product_update: OrderProductUpdateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    order_product = await crud.get_order_product(
        order_id=order_id, product_id=product_id, session=session
    )
    return await crud.update_profile(
        session=session,
        order_product_update=order_product_update,
        order_product=order_product,
    )


@router.delete("/{order_id}/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_product(
    order_id: int,
    product_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    order_product = await crud.get_order_product(
        order_id=order_id, product_id=product_id, session=session
    )
    await crud.delete_order_product(session=session, order_product=order_product)

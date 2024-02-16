from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.core.models import OrderProduct
from src.backend.app.order_products.schemas import OrderProductCreateSchema
from src.backend.app.order_products.schemas import OrderProductUpdateSchema


async def create_order_product(
    session: AsyncSession, order_product: OrderProductCreateSchema
) -> OrderProduct:
    """Create new order_product"""
    new_order_product = OrderProduct(
        order_id=order_product.order_id,
        product_id=order_product.product_id,
        quantity=order_product.quantity,
    )
    try:
        session.add(new_order_product)
        await session.commit()
        await session.refresh(new_order_product)
        return new_order_product
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_order_product(
    order_id: int,
    product_id: int,
    session: AsyncSession,
) -> OrderProduct | None:
    """Get order_product"""
    try:
        statement = (
            select(OrderProduct)
            .where(OrderProduct.order_id == order_id)
            .where(OrderProduct.product_id == product_id)
        )
        order_product: OrderProduct | None = await session.scalar(statement=statement)
        if not order_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order_product not found",
            )
        return order_product
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_order_products(session: AsyncSession) -> list[OrderProduct]:
    """Get all order_products"""
    try:
        statement = select(OrderProduct)
        result: Result = await session.execute(statement=statement)
        order_products = result.scalars().all()
        return list(order_products)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def update_profile(
    session: AsyncSession,
    order_product: OrderProduct,
    order_product_update: OrderProductUpdateSchema,
) -> OrderProduct:
    """Update order_product"""
    try:
        for name, value in order_product_update.model_dump(exclude_unset=True).items():
            setattr(order_product, name, value)
        await session.commit()
        await session.refresh(order_product)
        return order_product
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_order_product(
    session: AsyncSession, order_product: OrderProduct
) -> None:
    """Delete order_product"""
    try:
        await session.delete(order_product)
        await session.commit()
        return None
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )

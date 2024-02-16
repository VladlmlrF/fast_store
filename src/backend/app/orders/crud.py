from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.core.models import Order
from src.backend.app.orders.schemas import OrderCreateSchema
from src.backend.app.orders.schemas import OrderUpdateSchema


async def create_order(
    session: AsyncSession,
    order: OrderCreateSchema,
) -> Order:
    """Create new order"""
    new_order = Order(
        user_id=order.user_id,
    )
    try:
        session.add(new_order)
        await session.commit()
        await session.refresh(new_order)
        return new_order
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_order(order_id: int, session: AsyncSession) -> Order | None:
    """Get order by id"""
    try:
        statement = select(Order).where(Order.id == order_id)
        order: Order | None = await session.scalar(statement=statement)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order {order_id} not found",
            )
        return order
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_orders(session: AsyncSession) -> list[Order]:
    """Get all orders"""
    try:
        statement = select(Order)
        result: Result = await session.execute(statement=statement)
        orders = result.scalars().all()
        return list(orders)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def update_order(
    session: AsyncSession,
    order: Order,
    order_update: OrderUpdateSchema,
) -> Order:
    """Update order"""
    try:
        for name, value in order_update.model_dump(exclude_unset=True).items():
            setattr(order, name, value)
        await session.commit()
        await session.refresh(order)
        return order
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_order(session: AsyncSession, order: Order) -> None:
    """Delete order"""
    try:
        await session.delete(order)
        await session.commit()
        return None
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )

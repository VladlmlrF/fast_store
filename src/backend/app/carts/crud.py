from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.carts.schemas import CartCreateSchema
from src.backend.app.core.models import Cart


async def create_cart(session: AsyncSession, cart: CartCreateSchema) -> Cart:
    """Create new cart"""
    new_cart = Cart(user_id=cart.user_id)
    try:
        session.add(new_cart)
        await session.commit()
        await session.refresh(new_cart)
        return new_cart
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_carts(session: AsyncSession) -> list[Cart]:
    """Get all carts"""
    try:
        statement = select(Cart)
        result: Result = await session.execute(statement=statement)
        carts = result.scalars().all()
        return list(carts)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_cart_by_id(cart_id: int, session: AsyncSession) -> Cart | None:
    """Get cart by id"""
    try:
        statement = select(Cart).where(Cart.id == cart_id)
        cart: Cart | None = await session.scalar(statement=statement)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cart {cart_id} not found",
            )
        return cart
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_cart(cart: Cart, session: AsyncSession) -> None:
    """Delete cart"""
    try:
        await session.delete(cart)
        await session.commit()
        return None
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )

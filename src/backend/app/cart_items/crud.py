from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.cart_items.schemas import CartItemCreateSchema
from src.backend.app.cart_items.schemas import CartItemUpdateSchema
from src.backend.app.core.models import CartItem


async def create_cart_item(
    session: AsyncSession, cart_item: CartItemCreateSchema
) -> CartItem:
    """Create new cart_item"""
    new_cart_item = CartItem(
        cart_id=cart_item.cart_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
    )
    try:
        session.add(new_cart_item)
        await session.commit()
        await session.refresh(new_cart_item)
        return new_cart_item
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_cart_item_by_id(
    cart_item_id: int, session: AsyncSession
) -> CartItem | None:
    """Get cart_item by id"""
    try:
        statement = select(CartItem).where(CartItem.id == cart_item_id)
        cart_item: CartItem | None = await session.scalar(statement=statement)
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cart_item {cart_item_id} not found",
            )
        return cart_item
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_cart_items(session: AsyncSession) -> list[CartItem]:
    """Get all cart_items"""
    try:
        statement = select(CartItem)
        result: Result = await session.execute(statement=statement)
        cart_items = result.scalars().all()
        return list(cart_items)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_cart_items_by_cart_id(
    cart_id: int, session: AsyncSession
) -> list[CartItem]:
    """Get cart_items by cart_id"""
    try:
        statement = select(CartItem).where(CartItem.cart_id == cart_id)
        result: Result = await session.execute(statement=statement)
        cart_items = result.scalars().all()
        return list(cart_items)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def update_cart_item(
    session: AsyncSession,
    cart_item: CartItem,
    cart_item_update: CartItemUpdateSchema,
) -> CartItem:
    """Update cart_item"""
    try:
        for name, value in cart_item_update.model_dump(exclude_unset=True).items():
            setattr(cart_item, name, value)
        await session.commit()
        await session.refresh(cart_item)
        return cart_item
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_cart_item(session: AsyncSession, cart_item: CartItem) -> None:
    """Delete cart_item"""
    try:
        await session.delete(cart_item)
        await session.commit()
        return None
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )

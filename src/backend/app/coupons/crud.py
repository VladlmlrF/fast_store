from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.core.models import Coupon
from src.backend.app.coupons.schemas import CouponCreateSchema
from src.backend.app.coupons.schemas import CouponUpdateSchema


async def create_coupon(
    session: AsyncSession,
    coupon: CouponCreateSchema,
) -> Coupon:
    """Create new coupon"""
    new_coupon = Coupon(
        code=coupon.code,
        discount=coupon.discount,
        valid_from=coupon.valid_from,
        valid_until=coupon.valid_until,
        active=coupon.active,
    )
    try:
        session.add(new_coupon)
        await session.commit()
        await session.refresh(new_coupon)
        return new_coupon
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_coupon_by_id(coupon_id: int, session: AsyncSession) -> Coupon | None:
    """Get coupon by id"""
    try:
        statement = select(Coupon).where(Coupon.id == coupon_id)
        coupon: Coupon | None = await session.scalar(statement=statement)
        if not coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Coupon {coupon_id} not found",
            )
        return coupon
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_coupon_by_code(coupon_code: str, session: AsyncSession) -> Coupon | None:
    """Get coupon by code"""
    try:
        statement = select(Coupon).where(Coupon.code == coupon_code)
        coupon: Coupon | None = await session.scalar(statement=statement)
        if not coupon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Coupon {coupon_code} not found",
            )
        return coupon
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_coupons(session: AsyncSession) -> list[Coupon]:
    """Get all coupons"""
    try:
        statement = select(Coupon)
        result: Result = await session.execute(statement=statement)
        coupons = result.scalars().all()
        return list(coupons)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def update_coupon(
    session: AsyncSession,
    coupon: Coupon,
    coupon_update: CouponUpdateSchema,
) -> Coupon:
    """Update coupon"""
    try:
        for name, value in coupon_update.model_dump(exclude_unset=True).items():
            setattr(coupon, name, value)
        await session.commit()
        await session.refresh(coupon)
        return coupon
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_coupon(session: AsyncSession, coupon: Coupon) -> None:
    """Delete coupon"""
    try:
        await session.delete(coupon)
        await session.commit()
        return None
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )

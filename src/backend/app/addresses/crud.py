from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.addresses.schemas import AddressCreateSchema
from src.backend.app.addresses.schemas import AddressUpdateSchema
from src.backend.app.core.models import Address


async def create_address(
    session: AsyncSession, address: AddressCreateSchema
) -> Address:
    """Create new address"""
    new_address = Address(
        profile_id=address.profile_id,
        street=address.street,
        city=address.city,
        state=address.state,
        postal_code=address.postal_code,
        country=address.country,
    )
    try:
        session.add(new_address)
        await session.commit()
        await session.refresh(new_address)
        return new_address
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_address(address_id: int, session: AsyncSession) -> Address | None:
    """Get address bu id"""
    try:
        statement = select(Address).where(Address.id == address_id)
        address: Address | None = await session.scalar(statement=statement)
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Address {address_id} not found",
            )
        return address
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_addresses(session: AsyncSession) -> list[Address]:
    """Get all addresses"""
    try:
        statement = select(Address)
        result: Result = await session.execute(statement=statement)
        addresses = result.scalars().all()
        return list(addresses)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def update_address(
    session: AsyncSession,
    address: Address,
    address_update: AddressUpdateSchema,
) -> Address:
    """Update address"""
    try:
        for name, value in address_update.model_dump(exclude_unset=True).items():
            setattr(address, name, value)
        await session.commit()
        await session.refresh(address)
        return address
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def delete_address(session: AsyncSession, address: Address) -> None:
    """Delete address"""
    try:
        await session.delete(address)
        await session.commit()
        return None
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )

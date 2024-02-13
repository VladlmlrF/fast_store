from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.categories.schemas import CategoryCreateSchema
from src.backend.app.categories.schemas import CategoryUpdateSchema
from src.backend.app.core.models import Category


async def create_category(
    session: AsyncSession, category: CategoryCreateSchema
) -> Category:
    """Create new category"""
    new_category = Category(name=category.name)
    try:
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        return new_category
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Category with that name already exists!",
        )


async def get_category_by_name(session: AsyncSession, name: str) -> Category | None:
    """Get category by name"""
    try:
        statement = select(Category).where(Category.name == name)
        category: Category | None = await session.scalar(statement=statement)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {name} not found",
            )
        return category
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_categories(session: AsyncSession) -> list[Category]:
    """Get all categories"""
    try:
        statement = select(Category)
        result: Result = await session.execute(statement=statement)
        categories = result.scalars().all()
        return list(categories)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def update_category(
    session: AsyncSession,
    category: Category,
    category_update: CategoryUpdateSchema,
) -> Category:
    """Update category"""
    try:
        for name, value in category_update.model_dump().items():
            setattr(category, name, value)
        await session.commit()
        await session.refresh(category)
        return category
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_category(session: AsyncSession, category: Category) -> None:
    """Delete category"""
    try:
        await session.delete(category)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.core.models import Review
from src.backend.app.reviews.schemas import ReviewCreateSchema
from src.backend.app.reviews.schemas import ReviewUpdateSchema


async def create_review(
    session: AsyncSession,
    review: ReviewCreateSchema,
) -> Review:
    """Create new review"""
    new_review = Review(
        product_id=review.product_id,
        review_text=review.review_text,
        rating=review.rating,
    )
    try:
        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)
        return new_review
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_review(review_id: int, session: AsyncSession) -> Review | None:
    """Get review"""
    try:
        statement = select(Review).where(Review.id == review_id)
        review: Review | None = await session.scalar(statement=statement)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review {review_id} not found",
            )
        return review
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_reviews(session: AsyncSession) -> list[Review]:
    """Get all reviews"""
    try:
        statement = select(Review)
        result: Result = await session.execute(statement=statement)
        reviews = result.scalars().all()
        return list(reviews)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_reviews_by_product(
    product_id: int, session: AsyncSession
) -> list[Review]:
    """Get all reviews"""
    try:
        statement = select(Review).where(Review.product_id == product_id)
        result: Result = await session.execute(statement=statement)
        reviews = result.scalars().all()
        return list(reviews)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def update_review(
    session: AsyncSession,
    review: Review,
    review_update: ReviewUpdateSchema,
) -> Review:
    """Update review"""
    try:
        for name, value in review_update.model_dump(exclude_unset=True).items():
            setattr(review, name, value)
        await session.commit()
        await session.refresh(review)
        return review
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_review(session: AsyncSession, review: Review) -> None:
    """Delete review"""
    try:
        await session.delete(review)
        await session.commit()
        return None
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )

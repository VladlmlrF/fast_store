from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.auth.utils import admin_required
from src.backend.app.auth.utils import get_current_user_name
from src.backend.app.core.models import db_helper
from src.backend.app.reviews import crud
from src.backend.app.reviews.schemas import ReviewCreateSchema
from src.backend.app.reviews.schemas import ReviewSchema
from src.backend.app.reviews.schemas import ReviewUpdateSchema

router = APIRouter(tags=["Review"])


@router.post(
    "/",
    response_model=ReviewSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    review_in: ReviewCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_review(session=session, review=review_in)


@router.get("/", response_model=list[ReviewSchema])
async def get_reviews(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.get_reviews(session=session)


@router.get("/product/{product_id}", response_model=list[ReviewSchema])
async def get_reviews_by_product(
    product_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_reviews_by_product(product_id=product_id, session=session)


@router.get("/{review_id}", response_model=ReviewSchema)
async def get_review(
    review_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_review(review_id=review_id, session=session)


@router.patch("/{review_id}", response_model=ReviewSchema)
async def update_review(
    review_id: int,
    review_update: ReviewUpdateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    review = await crud.get_review(review_id=review_id, session=session)
    return await crud.update_review(
        session=session, review=review, review_update=review_update
    )


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    review = await crud.get_review(review_id=review_id, session=session)
    await crud.delete_review(session=session, review=review)
    return None

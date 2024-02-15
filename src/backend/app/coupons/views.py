from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.auth.utils import admin_required
from src.backend.app.auth.utils import get_current_user_name
from src.backend.app.core.models import db_helper
from src.backend.app.coupons import crud
from src.backend.app.coupons.schemas import CouponCreateSchema
from src.backend.app.coupons.schemas import CouponSchema
from src.backend.app.coupons.schemas import CouponUpdateSchema

router = APIRouter(tags=["Coupon"])


@router.post(
    "/",
    response_model=CouponSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_coupon(
    coupon_in: CouponCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.create_coupon(session=session, coupon=coupon_in)


@router.get("/", response_model=list[CouponSchema])
async def get_coupons(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_coupons(session=session)


@router.get("/{coupon_id}", response_model=CouponSchema)
async def get_coupon_by_id(
    coupon_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_coupon_by_id(coupon_id=coupon_id, session=session)


@router.get("/code/{coupon_code}", response_model=CouponSchema)
async def get_coupon_by_code(
    coupon_code: str,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_coupon_by_code(coupon_code=coupon_code, session=session)


@router.patch("/{coupon_id}", response_model=CouponSchema)
async def update_coupon(
    coupon_id: int,
    coupon_update: CouponUpdateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    coupon = await crud.get_coupon_by_id(coupon_id=coupon_id, session=session)
    return await crud.update_coupon(
        session=session, coupon=coupon, coupon_update=coupon_update
    )


@router.delete("/{coupon_id}", response_model=CouponSchema)
async def delete_coupon(
    coupon_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    coupon = await crud.get_coupon_by_id(coupon_id=coupon_id, session=session)
    return await crud.delete_coupon(session=session, coupon=coupon)

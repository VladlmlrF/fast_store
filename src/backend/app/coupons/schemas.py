from datetime import datetime
from datetime import timedelta

from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from pydantic import field_validator


class CouponBaseSchema(BaseModel):
    code: str
    discount: int
    valid_from: datetime = datetime.utcnow()
    valid_until: datetime = datetime.utcnow() + timedelta(days=3)
    active: bool

    @field_validator("discount")
    def validate_discount(cls, value):
        if 0 <= int(value) <= 100:
            return value
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The discount must be greater than or equal to zero and less than or equal to one hundred!",
        )


class CouponCreateSchema(CouponBaseSchema):
    pass


class CouponUpdateSchema(CouponBaseSchema):
    code: str | None = None
    discount: int | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    active: bool | None = None


class CouponSchema(CouponBaseSchema):
    id: int

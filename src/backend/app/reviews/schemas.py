from pydantic import BaseModel

from src.backend.app.core.models.review import Rating


class ReviewBaseSchema(BaseModel):
    product_id: int
    review_text: str
    rating: Rating


class ReviewCreateSchema(ReviewBaseSchema):
    pass


class ReviewUpdateSchema(BaseModel):
    review_text: str | None = None
    rating: Rating | None = None


class ReviewSchema(ReviewBaseSchema):
    id: int

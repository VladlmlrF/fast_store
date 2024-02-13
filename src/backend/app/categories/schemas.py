from pydantic import BaseModel


class CategoryBaseSchema(BaseModel):
    name: str


class CategoryCreateSchema(CategoryBaseSchema):
    pass


class CategoryUpdateSchema(CategoryBaseSchema):
    pass


class CategorySchema(CategoryBaseSchema):
    id: int

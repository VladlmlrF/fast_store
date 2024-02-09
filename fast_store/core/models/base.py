from sqlmodel import Field
from sqlmodel import SQLModel

metadata = SQLModel.metadata


class Base(SQLModel):
    __abstract__ = True

    id: int | None = Field(default=None, primary_key=True)

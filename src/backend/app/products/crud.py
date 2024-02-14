from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.core.models import Product
from src.backend.app.products.schemas import ProductCreateSchema
from src.backend.app.products.schemas import ProductUpdateSchema


async def create_product(
    session: AsyncSession,
    product: ProductCreateSchema,
) -> Product:
    """Create new product"""
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id,
    )
    try:
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        return new_product
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


async def get_product(product_id: int, session: AsyncSession) -> Product | None:
    """Get product by name"""
    try:
        statement = select(Product).where(Product.id == product_id)
        product: Product | None = await session.scalar(statement=statement)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {product_id} not found",
            )
        return product
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def get_products(session: AsyncSession) -> list[Product]:
    """Get all products"""
    try:
        statement = select(Product)
        result: Result = await session.execute(statement=statement)
        products = result.scalars().all()
        return list(products)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def update_product(
    session: AsyncSession,
    product: Product,
    product_update: ProductUpdateSchema,
) -> Product:
    """Update product"""
    try:
        for name, value in product_update.model_dump(exclude_unset=True).items():
            setattr(product, name, value)
        await session.commit()
        await session.refresh(product)
        return product
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )


async def delete_product(session: AsyncSession, product: Product) -> None:
    """Delete product"""
    try:
        await session.delete(product)
        await session.commit()
        return None
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        )

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.backend.app.addresses import crud
from src.backend.app.addresses.schemas import AddressCreateSchema
from src.backend.app.addresses.schemas import AddressSchema
from src.backend.app.addresses.schemas import AddressUpdateSchema
from src.backend.app.auth.utils import admin_required
from src.backend.app.auth.utils import get_current_user_name
from src.backend.app.core.models import db_helper

router = APIRouter(tags=["Address"])


@router.post("/", response_model=AddressSchema, status_code=status.HTTP_201_CREATED)
async def create_address(
    address_in: AddressCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.create_address(session=session, address=address_in)


@router.get("/", response_model=list[AddressSchema])
async def get_addresses(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.get_addresses(session=session)


@router.get("/{address_id}", response_model=AddressSchema)
async def get_address(
    address_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    return await crud.get_address(address_id=address_id, session=session)


@router.patch("/{address_id}", response_model=AddressSchema)
async def update_address(
    address_id: int,
    address_update: AddressUpdateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    address = await crud.get_address(address_id=address_id, session=session)
    return await crud.update_address(
        session=session, address=address, address_update=address_update
    )


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_name: str | None = Depends(get_current_user_name),
):
    await admin_required(session=session, current_user_name=current_user_name)
    address = await crud.get_address(address_id=address_id, session=session)
    await crud.delete_address(session=session, address=address)
    return None

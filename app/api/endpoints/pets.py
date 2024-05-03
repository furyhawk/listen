from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Pet, User
from app.schemas.requests import PetCreateRequest
from app.schemas.responses import PetResponse

router = APIRouter()


@router.post(
    "/create",
    response_model=PetResponse,
    status_code=status.HTTP_201_CREATED,
    description="Creates new pet. Only for logged users.",
)
async def create_new_pet(
    data: PetCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> Pet:
    new_pet = Pet(user_id=current_user.user_id, pet_name=data.pet_name)

    session.add(new_pet)
    await session.commit()

    return new_pet


@router.get(
    "/me",
    response_model=list[PetResponse],
    status_code=status.HTTP_200_OK,
    description="Get list of pets for currently logged user.",
)
async def get_all_my_pets(
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> list[Pet]:
    pets = await session.scalars(
        select(Pet).where(Pet.user_id == current_user.user_id).order_by(Pet.pet_name)
    )

    return list(pets.all())

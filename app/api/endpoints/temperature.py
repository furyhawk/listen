from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Temperature
from app.schemas.requests import MqttCreateRequest
from app.schemas.responses import TemperatureResponse


router = APIRouter()


@router.post(
    "/create",
    response_model=TemperatureResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create new temperature.",
)
async def create_temperature(
    data: MqttCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
) -> Temperature:
    new_temperature = Temperature(temperature=data.payload)
    session.add(new_temperature)
    await session.commit()
    return new_temperature


@router.get(
    "/all",
    response_model=list[TemperatureResponse],
    status_code=status.HTTP_200_OK,
    description="Get temperature of the city.",
)
async def get_temperature(
    session: AsyncSession = Depends(deps.get_session),
) -> list[Temperature]:
    temperature_list = await session.scalars(
        select(Temperature).order_by(Temperature.create_time.desc())
    )
    return list(temperature_list.all())

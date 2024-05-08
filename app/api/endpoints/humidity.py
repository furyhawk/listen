from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Humidity
from app.schemas.requests import MqttCreateRequest
from app.schemas.responses import HumidityResponse


router = APIRouter()


@router.post(
    "/create",
    response_model=HumidityResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create new humidity.",
)
async def create_new_humidity(
    data: MqttCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
) -> Humidity:
    new_humidity = Humidity(humidity=data.payload)
    session.add(new_humidity)
    await session.commit()
    return new_humidity


@router.get(
    "/all",
    response_model=list[HumidityResponse],
    status_code=status.HTTP_200_OK,
    description="Get humidity of the city.",
)
async def get_humidity(
    session: AsyncSession = Depends(deps.get_session),
) -> list[Humidity]:
    humidity_list = await session.scalars(
        select(Humidity).order_by(Humidity.create_time.desc())
    )
    return list(humidity_list.all())

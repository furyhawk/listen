from fastapi import APIRouter, Depends, status
from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Pressure
from app.schemas.requests import MqttCreateRequest
from app.schemas.responses import PressureResponse


router = APIRouter()


@router.post(
    "/create",
    response_model=PressureResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create new pressure.",
)
async def create_new_pressure(
    data: MqttCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
) -> Pressure:
    new_pressure = Pressure(pressure=data.payload)
    session.add(new_pressure)
    await session.commit()
    return new_pressure


@router.get(
    "/all",
    response_model=list[PressureResponse],
    status_code=status.HTTP_200_OK,
    description="Get pressure of the city.",
)
async def get_pressure(
    session: AsyncSession = Depends(deps.get_session),
) -> list[Pressure]:
    pressure_list: ScalarResult[Pressure] = await session.scalars(
        select(Pressure).order_by(Pressure.create_time.desc())
    )
    return list(pressure_list.all())

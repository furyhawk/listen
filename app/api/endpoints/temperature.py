from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
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
async def create_new_temperature(
    data: MqttCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
) -> Temperature:
    new_temperature = Temperature(temperature=data.payload)
    session.add(new_temperature)
    await session.commit()
    return new_temperature


@router.get(
    "/search",
    response_model=list[TemperatureResponse],
    status_code=status.HTTP_200_OK,
    description="Search temperature readings with optional date range, limit, and offset pagination.",
)
async def search_temperature(
    session: AsyncSession = Depends(deps.get_session),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    start_date: datetime | None = Query(
        None, description="Filter readings from this date (ISO 8601)"
    ),
    end_date: datetime | None = Query(
        None, description="Filter readings until this date (ISO 8601)"
    ),
) -> list[Temperature]:
    query = select(Temperature)

    if start_date:
        query = query.where(Temperature.create_time >= start_date)
    if end_date:
        query = query.where(Temperature.create_time <= end_date)

    query = query.order_by(Temperature.create_time.desc()).offset(offset).limit(limit)
    temperature_list = await session.scalars(query)
    return list(temperature_list.all())

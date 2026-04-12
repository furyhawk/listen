from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
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
    "/search",
    response_model=list[HumidityResponse],
    status_code=status.HTTP_200_OK,
    description="Search humidity readings with optional date range and limit.",
)
async def search_humidity(
    session: AsyncSession = Depends(deps.get_session),
    limit: int = Query(100, ge=1, le=1000),
    start_date: datetime | None = Query(None, description="Filter readings from this date (ISO 8601)"),
    end_date: datetime | None = Query(None, description="Filter readings until this date (ISO 8601)"),
) -> list[Humidity]:
    query = select(Humidity)
    
    if start_date:
        query = query.where(Humidity.create_time >= start_date)
    if end_date:
        query = query.where(Humidity.create_time <= end_date)
    
    query = query.order_by(Humidity.create_time.desc()).limit(limit)
    humidity_list = await session.scalars(query)
    return list(humidity_list.all())

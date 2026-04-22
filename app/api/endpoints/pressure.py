from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
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
    "/search",
    response_model=list[PressureResponse],
    status_code=status.HTTP_200_OK,
    description="Search pressure readings with optional date range and limit.",
)
async def search_pressure(
    session: AsyncSession = Depends(deps.get_session),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    start_date: datetime | None = Query(
        None, description="Filter readings from this date (ISO 8601)"
    ),
    end_date: datetime | None = Query(
        None, description="Filter readings until this date (ISO 8601)"
    ),
) -> list[Pressure]:
    query = select(Pressure)

    if start_date:
        query = query.where(Pressure.create_time >= start_date)
    if end_date:
        query = query.where(Pressure.create_time <= end_date)

    query = query.order_by(Pressure.create_time.desc()).offset(offset).limit(limit)
    pressure_list: ScalarResult[Pressure] = await session.scalars(query)
    return list(pressure_list.all())

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import IoTDevice, IoTReading
from app.schemas.requests import IoTLogRequest
from app.schemas.responses import IoTLogResponse

router = APIRouter()


@router.post(
    "/log",
    response_model=IoTLogResponse,
    status_code=status.HTTP_201_CREATED,
    description="Log batch IoT device sensor readings received from MQTT",
)
async def log_iot_readings(
    data: IoTLogRequest, session: AsyncSession = Depends(deps.get_session)
) -> dict[str, int]:
    total = 0

    for device in data.devices:
        existing = await session.scalar(
            select(IoTDevice).where(IoTDevice.device_id == device.device_id)
        )
        if existing is None:
            new_dev = IoTDevice(device_id=device.device_id)
            session.add(new_dev)

        for r in device.readings:
            new_reading = IoTReading(
                device_id=device.device_id, sensor_type=r.sensor_type, value=r.value
            )
            session.add(new_reading)
            total += 1

    await session.commit()
    return {"logged_count": total}

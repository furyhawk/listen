import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import IoTReading


@pytest.mark.asyncio(loop_scope="session")
async def test_log_iot_readings_single_device(client: AsyncClient, session: AsyncSession) -> None:
    payload = {
        "devices": [
            {"device_id": "dev-1", "readings": [{"sensor_type": "temperature", "value": "25.5"}]}
        ]
    }

    response = await client.post(app.url_path_for("log_iot_readings"), json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["logged_count"] == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_log_iot_readings_persists_multiple(client: AsyncClient, session: AsyncSession) -> None:
    payload = {
        "devices": [
            {"device_id": "dev-2", "readings": [
                {"sensor_type": "temperature", "value": "21.0"},
                {"sensor_type": "humidity", "value": "60%"}
            ]},
            {"device_id": "dev-3", "readings": [
                {"sensor_type": "pressure", "value": "1001"}
            ]},
        ]
    }

    response = await client.post(app.url_path_for("log_iot_readings"), json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    expected_count = sum(len(d["readings"]) for d in payload["devices"])
    assert response.json()["logged_count"] == expected_count

    rows = await session.scalars(select(IoTReading))
    all_readings = list(rows.all())
    assert len(all_readings) >= expected_count

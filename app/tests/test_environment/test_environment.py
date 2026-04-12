from datetime import datetime, timedelta

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import Humidity, Pressure, Temperature

MIN_EXPECTED_RESULTS = 2


@pytest.mark.asyncio(loop_scope="session")
async def test_create_new_temperature(client: AsyncClient) -> None:
    response = await client.post(
        app.url_path_for("create_new_temperature"),
        json={
            "publish_received_at": 1714785223633,
            "pub_props": {"User-Property": {}},
            "peerhost": "192.168.50.1",
            "qos": 0,
            "topic": "temperature",
            "clientid": "e661a4d4177d8a2a",
            "payload": "25.0",
            "username": "user1",
            "event": "message.publish",
            "metadata": {"rule_id": "sink_WH_D"},
            "timestamp": 1714785223633,
            "node": "emqx@node1.emqx.io",
            "id": "000617968C1EEAD9DB5B00000CFD0E24",
            "flags": {"retain": False, "dup": False},
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    result = response.json()
    assert result["temperature"] == "25.0"


@pytest.mark.asyncio(loop_scope="session")
async def test_search_temperature(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    temperature1 = Temperature(temperature="25.0")
    temperature2 = Temperature(temperature="26.0")

    session.add(temperature1)
    session.add(temperature2)
    await session.commit()

    response = await client.get(
        app.url_path_for("search_temperature"),
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= MIN_EXPECTED_RESULTS


@pytest.mark.asyncio(loop_scope="session")
async def test_search_temperature_with_limit(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    response = await client.get(
        app.url_path_for("search_temperature"),
        params={"limit": 1},
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) <= 1


@pytest.mark.asyncio(loop_scope="session")
async def test_search_temperature_with_date_range(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    now = datetime.utcnow()
    start_date = (now - timedelta(days=1)).isoformat() + "Z"
    end_date = (now + timedelta(days=1)).isoformat() + "Z"

    response = await client.get(
        app.url_path_for("search_temperature"),
        params={"start_date": start_date, "end_date": end_date},
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_new_pressure(client: AsyncClient) -> None:
    response = await client.post(
        app.url_path_for("create_new_pressure"),
        json={
            "publish_received_at": 1714785223633,
            "pub_props": {"User-Property": {}},
            "peerhost": "192.168.50.1",
            "qos": 0,
            "topic": "pressure",
            "clientid": "e661a4d417",
            "payload": "1000.0",
            "username": "user1",
            "event": "message.publish",
            "metadata": {"rule_id": "sink_WH_D"},
            "timestamp": 1714785223633,
            "node": "emqx@node1.emqx.io",
            "id": "000617968C1EEAD9DB5B00000CFD0E24",
            "flags": {"retain": False, "dup": False},
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    result = response.json()
    assert result["pressure"] == "1000.0"


@pytest.mark.asyncio(loop_scope="session")
async def test_search_pressure(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    pressure1 = Pressure(pressure="1000.0")
    pressure2 = Pressure(pressure="1001.0")

    session.add(pressure1)
    session.add(pressure2)
    await session.commit()

    response = await client.get(
        app.url_path_for("search_pressure"),
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= MIN_EXPECTED_RESULTS


@pytest.mark.asyncio(loop_scope="session")
async def test_search_pressure_with_limit(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    response = await client.get(
        app.url_path_for("search_pressure"),
        params={"limit": 1},
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) <= 1


@pytest.mark.asyncio(loop_scope="session")
async def test_create_new_humidity(client: AsyncClient) -> None:
    response = await client.post(
        app.url_path_for("create_new_humidity"),
        json={
            "publish_received_at": 1714785223633,
            "pub_props": {"User-Property": {}},
            "peerhost": "192.168.50.1",
            "qos": 0,
            "topic": "pressure",
            "clientid": "e661a4d417",
            "payload": "77.0",
            "username": "user1",
            "event": "message.publish",
            "metadata": {"rule_id": "sink_WH_D"},
            "timestamp": 1714785223633,
            "node": "emqx@node1.emqx.io",
            "id": "000617968C1EEAD9DB5B00000CFD0E24",
            "flags": {"retain": False, "dup": False},
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    result = response.json()
    assert result["humidity"] == "77.0"


@pytest.mark.asyncio(loop_scope="session")
async def test_search_humidity(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    humidity1 = Humidity(humidity="77.0")
    humidity2 = Humidity(humidity="78.0")

    session.add(humidity1)
    session.add(humidity2)
    await session.commit()

    response = await client.get(
        app.url_path_for("search_humidity"),
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= MIN_EXPECTED_RESULTS


@pytest.mark.asyncio(loop_scope="session")
async def test_search_humidity_with_limit(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    response = await client.get(
        app.url_path_for("search_humidity"),
        params={"limit": 1},
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) <= 1

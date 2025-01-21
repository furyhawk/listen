import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import Pet, User


@pytest.mark.asyncio(loop_scope="session")
async def test_create_new_pet(
    client: AsyncClient, default_user_headers: dict[str, str], default_user: User
) -> None:
    response = await client.post(
        app.url_path_for("create_new_pet"),
        headers=default_user_headers,
        json={"pet_name": "Tadeusz"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    result = response.json()
    assert result["user_id"] == default_user.user_id
    assert result["pet_name"] == "Tadeusz"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_my_pets(
    client: AsyncClient,
    default_user_headers: dict[str, str],
    default_user: User,
    session: AsyncSession,
) -> None:
    pet1 = Pet(user_id=default_user.user_id, pet_name="Pet_1")
    pet2 = Pet(user_id=default_user.user_id, pet_name="Pet_2")

    session.add(pet1)
    session.add(pet2)
    await session.commit()

    response = await client.get(
        app.url_path_for("get_all_my_pets"),
        headers=default_user_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [
        {
            "user_id": pet1.user_id,
            "pet_name": pet1.pet_name,
            "id": pet1.id,
        },
        {
            "user_id": pet2.user_id,
            "pet_name": pet2.pet_name,
            "id": pet2.id,
        },
    ]

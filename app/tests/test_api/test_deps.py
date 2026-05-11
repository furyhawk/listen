import types
from typing import Any, cast

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import api_messages, deps


class FakeSession:
    async def scalar(self, _query: Any) -> Any:
        return None


@pytest.mark.asyncio
async def test_get_current_user_raises_when_user_removed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # make verify_jwt_token return an object with .sub
    monkeypatch.setattr(
        deps,
        "verify_jwt_token",
        lambda token: types.SimpleNamespace(sub="non-existent"),
    )

    with pytest.raises(HTTPException) as excinfo:
        await deps.get_current_user(
            token="ignored", session=cast(AsyncSession, FakeSession())
        )

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == api_messages.JWT_ERROR_USER_REMOVED

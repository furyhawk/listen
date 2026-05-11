import types

import pytest
from fastapi import HTTPException

from app.api import deps
from app.api import api_messages


class FakeSession:
    async def scalar(self, _query):
        return None


@pytest.mark.asyncio
async def test_get_current_user_raises_when_user_removed(monkeypatch):
    # make verify_jwt_token return an object with .sub
    monkeypatch.setattr(deps, "verify_jwt_token", lambda token: types.SimpleNamespace(sub="non-existent"))

    with pytest.raises(HTTPException) as excinfo:
        await deps.get_current_user(token="ignored", session=FakeSession())

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == api_messages.JWT_ERROR_USER_REMOVED

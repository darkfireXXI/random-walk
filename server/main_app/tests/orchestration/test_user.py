from uuid import UUID

import pytest
from orchestration import user as user_orchestration


@pytest.mark.usefixtures("clean_db", autouse=True)
@pytest.mark.asyncio(loop_scope="session")
async def test_upsert_user(generate_user):
    user = await generate_user()
    user_json = await user_orchestration.upsert_user(user.to_view())

    assert isinstance(user_json, dict)
    assert user.uuid == UUID(user_json["uuid"])

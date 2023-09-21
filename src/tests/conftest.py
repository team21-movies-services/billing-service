import asyncio

import pytest

pytest_plugins = (
    "tests.app.functional.plugins.api_client",
    "tests.app.functional.plugins.auth_user",
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

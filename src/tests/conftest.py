import asyncio

import pytest

pytest_plugins = ("tests.plugins.api_client", "tests.plugins.auth_user")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

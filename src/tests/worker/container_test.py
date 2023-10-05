import pytest
from worker.container import app
from worker.services import PaymentStatusService, SubscriptionService

classes_to_resolve = [
    PaymentStatusService,
    SubscriptionService,
]


@pytest.mark.parametrize('cls', classes_to_resolve)
def test_container(cls):
    instance = app.resolve(cls)
    assert isinstance(instance, cls)

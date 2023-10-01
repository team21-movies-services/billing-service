from worker.container import app
from worker.services.payment import PaymentStatusService


def test_container():
    payment_service = app.resolve(PaymentStatusService)
    assert isinstance(payment_service, PaymentStatusService)

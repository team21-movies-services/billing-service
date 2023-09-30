import logging
from dataclasses import dataclass
from typing import TypeVar

from pydantic import BaseModel
from worker.providers import YookassaPaymentProvider
from worker.providers.mock_provider import MockPaymentProvider
from worker.schemas.payment import PaymentSchema

logger = logging.getLogger(__name__)

A = TypeVar("A", BaseModel, PaymentSchema)


@dataclass
class EventHandler:
    _yookassa_provider: YookassaPaymentProvider
    _mock_provider: MockPaymentProvider

    def handle_event(self, event: A) -> A | None:
        match event.model_dump():
            case {"system": "yookassa"}:
                return self._yookassa_provider.get_payment_status(event)
            case {"system": "mock"}:
                logger.debug("Handling mock event")
                return self._mock_provider.get_payment_status(event)
            case _:
                logger.debug(event)
                logger.error("Unknown event")
                return None

import logging
from dataclasses import dataclass

from worker.providers import BasePaymentProvider, YookassaPaymentProvider
from worker.providers.mock_provider import MockPaymentProvider

logger = logging.getLogger(__name__)


@dataclass
class ProviderFactory:
    _yookassa_provider: YookassaPaymentProvider
    _mock_provider: MockPaymentProvider

    def get_payment_provider(self, provider_name: str) -> BasePaymentProvider:
        match provider_name:
            case "yookassa":
                return self._yookassa_provider
            case "mock":
                logger.debug("Handling mock event")
                return self._mock_provider
            case _:
                raise ValueError("Unknown payment provider %s", provider_name)

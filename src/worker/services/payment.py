import logging
from dataclasses import dataclass

from worker.core.config import Settings
from worker.event_handler import EventHandler
from worker.repository.payment import UserPaymentsRepository

logger = logging.getLogger(__name__)


@dataclass
class PaymentStatusService:
    """
    Сервис для работы со статусами платежей.

    Используется для обновления статусов платежей, основанных на
    событиях и изменениях, обрабатываемых внутренним механизмом.

    Attributes:
        _payment_repository: Репозиторий для работы с платежами.
        _event_handler: Сортирует платежи для обработки в нужных провайдерах.
    """

    _payment_repository: UserPaymentsRepository
    _event_handler: EventHandler
    _settings: Settings

    def update_pending_payments(self):
        """
        Обновляет платежи со статусом "pending".

        Для каждого платежа со статусом "pending" метод:
        1. Уточняет статус платежа у провайдера.
        2. Проверяет на наличие изменений.
        3. Обновляет статус платежа, если он изменился после обработки события.

        Returns:
            Обновленный объект платежа, если статус был изменен, иначе оригинальный объект платежа.
        """
        payment_gen = self._payment_repository.get_payments_with_status("failed")
        for payment in payment_gen:
            updated_payment = self._event_handler.handle_event(payment)
            if updated_payment:
                is_updated = self._payment_repository.set_payment_status(payment)
                if is_updated:
                    logger.info("Updated payment with id %s to status %s", updated_payment.id, updated_payment.status)
        logger.info("Payments checked, next check in %s minute(s)", self._settings.worker.pending_payments_check)

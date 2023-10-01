import logging.config
from datetime import timedelta
from time import sleep

from scheduler.threading.scheduler import Scheduler
from worker.container import app, settings
from worker.core.logger import Logger
from worker.services.payment import PaymentStatusService
from yookassa import Configuration

logging.config.dictConfig(app.resolve(Logger).get_settings())
logger = logging.getLogger(__name__)


PENDING_PAYMENTS_CHECK_INTERVAL = timedelta(seconds=settings.worker.pending_payments_check)


# Конфигурация SDK Юкассы
Configuration.configure(settings.yookassa.shop_id, settings.yookassa.api_key)


def main():
    scheduler = Scheduler()
    payment_service: PaymentStatusService = app.resolve(PaymentStatusService)
    scheduler.cyclic(PENDING_PAYMENTS_CHECK_INTERVAL, payment_service.update_pending_payments)
    while True:
        scheduler.exec_jobs()
        sleep(1)


if __name__ == '__main__':
    main()

import logging.config
from datetime import timedelta
from time import sleep

from scheduler import Scheduler
from worker.container import app
from worker.core.config import Settings
from worker.core.logger import Logger
from worker.services.payment import PaymentStatusService

logging.config.dictConfig(app.resolve(Logger).get_settings())
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    scheduler = Scheduler()
    settings = app.resolve(Settings)
    service: PaymentStatusService = app.resolve(PaymentStatusService)
    scheduler.cyclic(timedelta(minutes=settings.worker.pending_payments_check), service.update_pending_payments)
    while True:
        scheduler.exec_jobs()
        sleep(1)

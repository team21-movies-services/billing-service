import logging.config
from time import sleep

from scheduler.container import app
from scheduler.core.logger import Logger

from services.payment import PaymentStatusService

logging.config.dictConfig(app.resolve(Logger).get_settings())
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    service: PaymentStatusService = app.resolve(PaymentStatusService)
    while True:
        service.check_payments()
        sleep(10)

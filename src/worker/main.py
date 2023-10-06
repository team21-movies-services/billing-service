import logging.config
from datetime import time, timedelta
from time import sleep

from scheduler.threading.scheduler import Scheduler
from worker.container import app, settings
from worker.core.logger import Logger
from worker.services import PaymentStatusService, SentryService, SubscriptionService

logging.config.dictConfig(app.resolve(Logger).get_settings())
logger = logging.getLogger(__name__)


PENDING_PAYMENTS_CHECK_INTERVAL = timedelta(seconds=settings.worker.pending_payments_check)
DISABLE_SUBSCRIPTIONS_INTERVAL = time(hour=settings.worker.disable_subs_h, minute=settings.worker.disable_subs_m)


def main():
    scheduler = Scheduler()
    payment_service: PaymentStatusService = app.resolve(PaymentStatusService)
    if settings.sentry.enable:
        sentry_service = app.resolve(SentryService)
        sentry_service.start_sentry()
    scheduler.cyclic(PENDING_PAYMENTS_CHECK_INTERVAL, payment_service.update_pending_payments_and_activate_subs)

    subscription_service = app.resolve(SubscriptionService)
    scheduler.daily(DISABLE_SUBSCRIPTIONS_INTERVAL, subscription_service.disable, alias="Subscriptions disable")
    scheduler.cyclic(PENDING_PAYMENTS_CHECK_INTERVAL, subscription_service.make_recurrent_payment)
    while True:
        scheduler.exec_jobs()
        sleep(1)


if __name__ == '__main__':
    main()

from rodi import Container
from shared.clients import BaseHttpClient, HttpxHttpClient
from shared.core.config import SharedSettings
from shared.providers.payments import (
    MockPaymentProvider,
    ProviderFactory,
    YookassaPaymentProvider,
)
from shared.services import EventSenderService
from shared.settings import YookassaBaseConfig
from worker.clients import DbClientABC, SQLAlchemyDbClient
from worker.core.config import Settings
from worker.core.logger import Logger
from worker.services.payment import PaymentStatusService
from worker.services.sentry import SentryService
from worker.services.subscription import SubscriptionService
from worker.uow.uow import SqlAlchemyUoW, UnitOfWorkABC

app = Container()
settings = Settings()
shared_settings = SharedSettings()

app.register(Settings, instance=settings)
app.register(YookassaBaseConfig, instance=settings.yookassa)
app.register(SharedSettings, instance=shared_settings)


# Logging
app.register(Logger)

# Clients
app.add_singleton(DbClientABC, SQLAlchemyDbClient)
app.register(BaseHttpClient, HttpxHttpClient)

# PaymentProvider
app.register(YookassaPaymentProvider)
app.register(MockPaymentProvider)

# Services
app.register(PaymentStatusService)
app.register(SentryService)
app.register(SubscriptionService)
app.register(EventSenderService)

# EventHandler
app.register(ProviderFactory)

# UoW
app.register(UnitOfWorkABC, SqlAlchemyUoW)

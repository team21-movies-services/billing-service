from rodi import Container
from shared.clients import BaseHttpClient, HttpxHttpClient
from shared.services import EventSenderService
from worker.clients import DbClientABC, SQLAlchemyDbClient
from worker.core.config import Settings
from worker.core.logger import Logger
from worker.providers import (
    MockPaymentProvider,
    ProviderFactory,
    YookassaPaymentProvider,
)
from worker.services import PaymentStatusService, SubscriptionService
from worker.services.sentry import SentryService
from worker.uow import SqlAlchemyUoW, UnitOfWorkABC

app = Container()
settings = Settings()

app.register(Settings, instance=settings)


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

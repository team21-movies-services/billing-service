from rodi import Container
from shared.providers.payments.factory import ProviderFactory
from shared.providers.payments.mock_provider import MockPaymentProvider
from shared.providers.payments.yookassa_provider import YookassaPaymentProvider
from worker.clients.database.base_db_client import DbClientABC
from worker.clients.database.pg_client import SQLAlchemyDbClient
from worker.core.config import Settings
from worker.core.logger import Logger
from worker.services.payment import PaymentStatusService
from worker.services.sentry import SentryService
from worker.services.subscription import SubscriptionService
from worker.uow.uow import SqlAlchemyUoW, UnitOfWorkABC

app = Container()
settings = Settings()

app.register(Settings, instance=settings)


# Logging
app.register(Logger)

# Clients
app.add_singleton(DbClientABC, SQLAlchemyDbClient)

# PaymentProvider
app.register(YookassaPaymentProvider)
app.register(MockPaymentProvider)

# Services
app.register(PaymentStatusService)
app.register(SentryService)
app.register(SubscriptionService)

# EventHandler
app.register(ProviderFactory)

# UoW
app.register(UnitOfWorkABC, SqlAlchemyUoW)

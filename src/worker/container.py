from rodi import Container
from worker.clients.database import SQLAlchemyProvider
from worker.core.config import Settings
from worker.core.logger import Logger
from worker.providers import MockPaymentProvider, YookassaPaymentProvider
from worker.providers.factory import ProviderFactory
from worker.repository.payment import UserPaymentsRepository
from worker.services.payment import PaymentStatusService
from worker.services.sentry import SentryService

app = Container()
settings = Settings()

app.register(Settings, instance=settings)

# Logging
app.register(Logger)

# Clients
app.add_singleton(SQLAlchemyProvider)

# Repository
app.register(UserPaymentsRepository)

# PaymentProvider
app.register(YookassaPaymentProvider)
app.register(MockPaymentProvider)

# Services
app.register(PaymentStatusService)
app.register(SentryService)

# EventHandler
app.register(ProviderFactory)

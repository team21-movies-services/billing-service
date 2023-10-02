from rodi import Container
from shared.providers.payments.factory import ProviderFactory
from shared.providers.payments.mock_provider import MockPaymentProvider
from shared.providers.payments.yookassa_provider import YookassaPaymentProvider
from worker.clients.database import SQLAlchemyProvider
from worker.core.config import Settings
from worker.core.logger import Logger
from worker.repository.payment import UserPaymentsRepository
from worker.services.payment import PaymentStatusService

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

# EventHandler
app.register(ProviderFactory)

from rodi import Container
from worker.clients import DbClientABC, SQLAlchemyDbClient
from worker.core.config import Settings
from worker.core.logger import Logger
from worker.providers import (
    MockPaymentProvider,
    ProviderFactory,
    YookassaPaymentProvider,
)
from worker.services import PaymentStatusService
from worker.uow import SqlAlchemyUoW, UnitOfWorkABC

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

# EventHandler
app.register(ProviderFactory)

# UoW
app.register(UnitOfWorkABC, SqlAlchemyUoW)

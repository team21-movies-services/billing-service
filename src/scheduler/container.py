import httpx
from rodi import Container
from scheduler.clients import SQLAlchemyProvider
from scheduler.clients.http_client import BaseHTTPClient, HTTPXClient
from scheduler.core.config import Settings
from scheduler.core.logger import Logger
from scheduler.providers.yookassa import BasePaymentProvider, YookassaProvider
from scheduler.repository.payment import UserPaymentsRepository

from services.payment import PaymentStatusService

app = Container()


def get_httpx_client() -> httpx.Client:
    return httpx.Client()


app.add_instance(Settings())
# Logging
app.register(Logger)
# Clients
app.register(BaseHTTPClient, HTTPXClient)
app.add_singleton(SQLAlchemyProvider)
app.add_singleton_by_factory(get_httpx_client)
# Repository
app.register(UserPaymentsRepository)
# PaymentProvider
app.register(BasePaymentProvider, YookassaProvider)
# Services
app.register(PaymentStatusService)

from app.dependencies.registrator import add_factory_to_mapper
from app.dependencies.repository_dependencies.payment import PaymentRepositoryDep
from app.services.payment import PaymentService, PaymentServiceABC


@add_factory_to_mapper(PaymentServiceABC)
def create_payment_service(payment_repository: PaymentRepositoryDep) -> PaymentService:
    return PaymentService(payment_repository)

from dependencies.registrator import add_factory_to_mapper
from dependencies.repository_dependencies.pay_system import PaySystemRepositoryDep
from services.pay_system import PaySystemService, PaySystemServiceABC


@add_factory_to_mapper(PaySystemServiceABC)
def create_pay_system_service(pay_system_repository: PaySystemRepositoryDep) -> PaySystemService:
    return PaySystemService(pay_system_repository)

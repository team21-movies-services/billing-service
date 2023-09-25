from app.dependencies.registrator import add_factory_to_mapper
from app.dependencies.repository_dependencies.tariff import TariffRepositoryDep
from app.services.tariff import TariffService, TariffServiceABC


@add_factory_to_mapper(TariffServiceABC)
def create_tariff_service(tariff_repository: TariffRepositoryDep) -> TariffService:
    return TariffService(tariff_repository)

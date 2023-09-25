from app.dependencies.registrator import add_factory_to_mapper
from app.services.status import StatusService, StatusServiceABC


@add_factory_to_mapper(StatusServiceABC)
def create_status_service() -> StatusService:
    return StatusService()

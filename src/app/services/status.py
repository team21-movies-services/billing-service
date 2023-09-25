from abc import ABC, abstractmethod

from app.schemas.response.status import StatusResponse


class StatusServiceABC(ABC):
    @abstractmethod
    async def get_api_status(self) -> StatusResponse:
        raise NotImplementedError


class StatusService(StatusServiceABC):
    async def get_api_status(self) -> StatusResponse:
        return StatusResponse(api=True)

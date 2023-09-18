from pydantic import BaseModel


class StatusRequest(BaseModel):
    api: str

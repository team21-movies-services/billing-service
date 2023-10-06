from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class YookassaBaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="YOOKASSA_")

    api_key: str = Field(default="")
    shop_id: str = Field(default="")
    return_url: str = Field(default="")

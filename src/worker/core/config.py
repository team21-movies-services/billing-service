from datetime import timezone

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="worker_")

    log_level: str = Field(default="DEBUG")
    pending_payments_check: int = Field(default=60)
    disable_subs_h: int = Field(default=19)
    disable_subs_m: int = Field(default=14)

    tz: timezone = Field(default=timezone.utc)


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='postgres_')

    echo_log: bool = Field(default=False)
    host: str = Field(default='localhost')
    port: int = Field(default=5432)
    db: str = Field(default='billing_database')
    user: str = Field(default='billing')
    password: str = Field(default='billing')

    @property
    def database_url(self):
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class YookassaConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="YOOKASSA_")

    api_key: str = Field(default="")
    shop_id: str = Field(default="")


class SentryConfig(BaseSettings):
    dsn: str = Field(default="dsn", alias='SENTRY_DSN')
    enable: bool = Field(default=False, alias='SENTRY_ENABLE')


class Settings(BaseSettings):
    worker: WorkerSettings = WorkerSettings()
    postgres: PostgresSettings = PostgresSettings()
    yookassa: YookassaConfig = YookassaConfig()
    sentry: SentryConfig = SentryConfig()

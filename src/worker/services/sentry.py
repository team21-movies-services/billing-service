from dataclasses import dataclass

import sentry_sdk
from worker.core.config import Settings


@dataclass
class SentryService:
    _settings: Settings

    def start_sentry(self):
        sentry_sdk.init(dsn=self._settings.sentry.dsn, traces_sample_rate=1.0, profiles_sample_rate=1.0)

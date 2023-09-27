from dataclasses import dataclass

from .config import Settings

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console']


@dataclass
class Logger:
    _settings: Settings

    def get_settings(self):
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': LOG_FORMAT,
                },
            },
            'handlers': {
                'console': {
                    'level': self._settings.project.log_level,
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                },
            },
            'loggers': {
                '': {
                    'handlers': LOG_DEFAULT_HANDLERS,
                    'level': self._settings.project.log_level,
                },
            },
            'root': {
                'level': self._settings.project.log_level,
                'formatter': 'verbose',
                'handlers': LOG_DEFAULT_HANDLERS,
            },
        }

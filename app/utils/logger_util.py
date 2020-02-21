import os
import sys

import loguru


class Logger():
    """
    日志记录工具类
    """

    def __init__(self, app=None):
        self._logger = loguru.logger
        self._app = app
        self._log_dir = None
        self._env = None

    def init_app(self, app):
        if self._app is None:
            self._app = app
        self._check_env()
        try:
            self._logger.remove(0)
        except Exception as e:
            pass
        if self._env == "development":
            self._init_dev()
        else:
            self._init_pro()
    def _check_env(self):
        logger_type = os.getenv("Logger_Type")
        log_dir = os.getenv("Log_Dir")

        if log_dir is None:
            self._log_dir = 'logs/'
        else:
            self._log_dir = log_dir

        if logger_type is not None:
            if logger_type == 'development':
                self._env = "development"
            elif logger_type == 'production':
                self._env = "production"
        else:
            raise ValueError("Missing required configuration data for 'Logger_Type'.")

    def _init_dev(self):
        self._logger.add(
            sys.stdout, colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> <bold>| {level} |</bold> {name}:{function}:{line} >>> {"
                   "message}",
            level='DEBUG'
        )

    def _init_pro(self):
        schema = f'{self._log_dir}' + 'CUUSP_{time:YYYY-MM-DD}.log'
        self._logger.add(schema, colorize=False,
                         format="{time:YYYY-MM-DD HH:mm:ss} |{level}| {name}:{function}:{line} >>> {message}",
                         rotation='00:00',
                         level='INFO',
                         retention='1 month'
                         )

    @property
    def logger(self):
        return self._logger

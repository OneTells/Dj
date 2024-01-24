from sys import stderr
from urllib.parse import unquote

from loguru import logger as loguru_logger

from core.config import LoggerInfo
from core.schemes.logger import Level


class Logger:
    __is_initialized: bool = False

    def __init__(self, user_id: int = 'System') -> None:
        self.__logger = loguru_logger.bind(user_id=user_id)

    def logging(self, level: Level, message: str) -> None:
        if not self.__class__.__is_initialized:
            self.__connect()

        try:
            self.__logger.__getattribute__(str(level.value))(unquote(message))
        except FileNotFoundError:
            pass

    @classmethod
    def __connect(cls) -> None:
        cls.__is_initialized = True

        loguru_logger.remove()
        loguru_logger.add(stderr, level="INFO", enqueue=True, format=LoggerInfo.FORMAT, backtrace=True, diagnose=True)
        loguru_logger.add(
            f'{LoggerInfo.PATH}/debug.log', level='DEBUG', rotation='1024 MB', format=LoggerInfo.FORMAT, backtrace=True,
            diagnose=True, enqueue=True, compression='tar.xz', retention='30 days'
        )

    def debug(self, message: str) -> None:
        self.logging(Level.DEBUG, message)

    def info(self, message: str) -> None:
        self.logging(Level.INFO, message)

    def success(self, message: str) -> None:
        self.logging(Level.SUCCESS, message)

    def warning(self, message: str) -> None:
        self.logging(Level.WARNING, message)

    def error(self, message: str) -> None:
        self.logging(Level.ERROR, message)

    def critical(self, message: str) -> None:
        self.logging(Level.CRITICAL, message)

    def exception(self, message: str = '') -> None:
        self.__logger.exception(message)


logger = Logger()

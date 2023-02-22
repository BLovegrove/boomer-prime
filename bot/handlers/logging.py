import logging
import logging.handlers
import sys


class LogHandler:
    def __init__(
        self, filename: str = "discord.log", log_level: int = logging.DEBUG
    ) -> None:

        self.formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name:<16}: {message}",
            "%Y-%m-%d %H:%M:%S",
            style="{",
        )

        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=filename, encoding="UTF-8", when="midnight"
        )
        file_handler.suffix = "%Y_%m_%d"
        term_handler = logging.StreamHandler(sys.stdout)

        custom_logger = logging.getLogger("bot")
        discord_logger = logging.getLogger("discord")

        file_handler.setFormatter(self.formatter)
        term_handler.setFormatter(self.formatter)

        custom_logger.addHandler(file_handler)
        custom_logger.addHandler(term_handler)
        custom_logger.setLevel(log_level)

        discord_logger.handlers.clear()
        discord_logger.addHandler(file_handler)
        discord_logger.setLevel(log_level)

        self.bot = custom_logger

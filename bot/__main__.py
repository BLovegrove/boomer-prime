import logging
import logging.handlers
import sys

from loguru import logger

import config as cfg

from .util.models import LavaBot


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# make sure the main py file is being run as a file and not imported
def main():
    bot = LavaBot()
    discord_logger = logging.getLogger("discord")
    for handler in discord_logger.handlers:
        discord_logger.removeHandler(handler)
    print(discord_logger.handlers)
    discord_logger.addHandler(InterceptHandler())
    logger.remove()
    logger_format = "<g>{time:YYYY-MM-DD HH:mm:ss}</> <c>|</> <lvl>{level.name:<8}</> <c>|</> <m>{name:<32}</><y>LINE:{line:<4}</> <c>|</> {message}"
    logger.add(sys.stdout, colorize=True, backtrace=True, format=logger_format)
    logger.add(
        sink="bot.log",
        rotation="1 day",
        compression="zip",
        colorize=True,
        enqueue=True,
        backtrace=True,
        format=logger_format,
    )
    bot.run(cfg.bot.token, log_formatter=None)


if __name__ == "__main__":
    main()

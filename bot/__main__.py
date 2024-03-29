import logging
import logging.handlers
import os
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


logging.basicConfig(handlers=[InterceptHandler()], level="INFO", force=True)


# make sure the main py file is being run as a file and not imported
def main():
    bot = LavaBot()
    logger.remove()
    logger_format = "<g>{time:YYYY-MM-DD HH:mm:ss}</> <c>|</> <lvl>{level.name:<8}</> <c>|</> <m>{name:<36}</><y>LINE:{line:<4}</> <c>|</> {message}"
    logger.add(
        sink="logs/bot.log",
        level="INFO",
        rotation="1 day",
        compression="zip",
        colorize=True,
        enqueue=True,
        format=logger_format,
        backtrace=True,
        diagnose=False,
    )
    logger.add(
        sink="logs/bot-debug.log",
        level="DEBUG",
        rotation="1 day",
        compression="zip",
        colorize=True,
        enqueue=True,
        format=logger_format,
        backtrace=True,
        diagnose=False,
    )
    bot.run(cfg.bot.token, log_handler=None)
    logger.warning(
        "# ---------------------------------------------------------------------------- #"
    )
    logger.warning(
        "#                             BOT SHUTDOWN COMPLETE                            #"
    )
    logger.warning(
        "# ---------------------------------------------------------------------------- #"
    )


if __name__ == "__main__":
    main()

import os
import pathlib
import sys

from loguru import logger

import config as cfg

print(pathlib.Path(__file__).stem)


def main():
    logger.remove()
    logger.add(
        sink="bot.log",
        rotation="1 day",
        compression="zip",
        colorize=True,
        enqueue=True,
        backtrace=True,
        format="{time:YYYY-MM-DD HH:mm:ss} | <lvl>{level.name:<8}</> | {file.name:<18}#{line} | {message}",
    )
    logger.debug("Hello world!")
    logger.info("Hello world!")
    logger.warning("Hello world!")
    logger.error("Hello world!")
    logger.critical("Hello world!")

    try:
        print(str(13 / 0))
    except Exception:
        logger.exception("Well fuck.")


if __name__ == "__main__":
    main()

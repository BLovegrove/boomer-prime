import os
import pathlib
import sys

from loguru import logger

import config as cfg

print(pathlib.Path(__file__).stem)


class PlayerNotFoundException(Exception):
    "Raised when an attempt to retrieve a Lavalink Player from the manager cache returns None"
    pass
    # def __init__(self, *args: object) -> None:
    #     logger.exception(
    #         "Failed to retrieve Player from PlayerManager cache", args=args
    #     )
    #     pass


def main():
    format = "{time:YYYY-MM-DD HH:mm:ss} | <lvl>{level.name:<8}</> | {file.name:<18}#{line} | {message}"
    logger.remove()
    logger.add(sys.stdout, enqueue=True, colorize=True, backtrace=True, format=format)
    logger.add(
        sink="test.log",
        rotation="1 day",
        compression="zip",
        colorize=True,
        enqueue=True,
        backtrace=True,
        format=format,
    )
    logger.debug("Hello world!")
    logger.info("Hello world!")
    logger.warning("Hello world!")
    logger.error("Hello world!")
    logger.critical("Hello world!")


if __name__ == "__main__":
    main()

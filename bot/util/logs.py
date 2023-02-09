import discord
import logging


def getLogger():
    # init logging and set some custom details
    handler = logging.FileHandler(filename="discord.log", encoding="UTF-8", mode="w")
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
    )
    handler.setFormatter(formatter)
    discord.utils.setup_logging(handler=handler, level=logging.INFO)
    return logging.getLogger("discord")

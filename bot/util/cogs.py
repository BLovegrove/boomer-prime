import os

from discord.ext import commands


def search() -> list[str]:

    events_list = []

    for folder in os.listdir(f"bot/cogs/."):
        for filename in os.listdir(f"bot/cogs/{folder}/."):
            if filename.endswith(".py"):
                events_list.append(f"bot.cogs.{folder}.{filename[:-3]}")

    return events_list

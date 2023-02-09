from discord.ext import commands
import os


def search() -> list[str]:

    list = []

    for folder in os.listdir(f"bot/cogs/."):
        for filename in os.listdir(f"bot/cogs/{folder}/."):
            if filename.endswith(".py"):
                list.append(f"bot.cogs.{folder}.{filename[:-3]}")

    return list

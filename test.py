import sqlite3

import discord

import config as cfg
from bot.handlers.database import DBHandler
from bot.util.models import LavaBot

bot = LavaBot()
dbh = DBHandler(bot)
favs = {
    "🍕 Pizza time": "https://www.youtube.com/watch?v=lpvT-Fciu-4",
    "🔥 Doom OST": "https://www.youtube.com/watch?v=EQmIBHObtCs",
    "🌎 Earthbound Guardian": "https://www.youtube.com/watch?v=6M-NkQAo-3E",
    "🪨 Roxanne (just rocks)": "https://www.youtube.com/watch?v=ZPjSV-lnqvg",
    "🪕 Bluegrass Banjo": "https://www.youtube.com/watch?v=85mDyWCgHy0",
    "🐦 Free Bird solo": "https://www.youtube.com/watch?v=5HeAgeyyCUA",
    "🥥 Coconut Mall(ding)": "https://www.youtube.com/watch?v=cscuCIzItZQ",
    "🔫 Big Iron Hip": "https://www.youtube.com/watch?v=dloboO5bWCA",
}

dbh.update_insert_favs(636752938412408835, favs)

# for key, value in favs.items():
#     print(f"{key}, {value}")

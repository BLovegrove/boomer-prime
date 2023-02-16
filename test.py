import sqlite3

import discord

conn = sqlite3.connect("bot.sqlite")
cursor = conn.cursor()


cursor.execute(
    "INSERT INTO bgm(member_id,track_url) VALUES(278441913361629195,'https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=1s')"
)

cursor.execute(
    "INSERT INTO favs(guild_role_id,list_data) VALUES(1001722386976084071,'╳name1◆https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=1s▶name2◆https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=1s▶name3◆https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=1s')"
)

conn.commit()

result = cursor.execute(
    "SELECT track_url FROM bgm WHERE member_id=278441913361629195"
).fetchone()
print(result[0])

result_ = cursor.execute("SELECT guild_role_id FROM favs").fetchall()
print(result_)


# import discord
# from discord.ext import commands

# import config as cfg
# from bot.handlers.database import DBHandler
# from bot.util import helper, models

# # logger = helper.logs.getLogger()


# # make sure the main py file is being run as a file and not imported
# def main():
#     bot = commands.Bot(commands.when_mentioned, intents=discord.Intents.all())
#     bot.run(cfg.bot.token)
#     member = bot.guilds[0].get_member(278441913361629195)
#     handler = DBHandler(bot)
#     favs = handler.fetch_favs(member)
#     print(favs)
#     handler.close()


# if __name__ == "__main__":
#     main()

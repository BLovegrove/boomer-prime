import sqlite3

import discord

from ..util.models import LavaBot
from ..util.transcoder import DictStrTranscoder


class DBHandler:
    def __init__(self, bot: LavaBot) -> None:
        pass

        self.bot = bot

        self.conn = sqlite3.connect("bot.sqlite")
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    # def bgm_insert(self, member: discord.Member, track_url: str)

    def bgm_fetch(self, member: discord.Member):

        result = self.cursor.execute(
            f"SELECT track_url FROM bgm WHERE member_id='{member.id}'"
        ).fetchone()[0]

        return result

    def fetch_favs(self, member: discord.Member):
        member_roles = member.roles
        available_favs: list[str] = self.cursor.execute(
            "SELECT guild_role_id FROM favs"
        ).fetchall()
        fav_ids: list[str] = []
        favs_data = ""
        for fav in available_favs:
            fav_ids.append(fav[0])
        fav_ids.reverse()
        for role in member_roles:
            if str(role.id) in fav_ids:
                favs_data: str = self.cursor.execute(
                    f"SELECT list_data FROM favs WHERE guild_role_id='{role.id}'"
                ).fetchone()[0]

        if favs_data == "":
            # TODO: some error checking here
            self.bot.logger.error("failed to grab fav list data")
            return

        favs = DictStrTranscoder.decode(favs_data)
        if not favs:
            return

        return favs

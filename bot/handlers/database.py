import sqlite3

import discord
from loguru import logger

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

    def fetch_bgm(self, member_id: str):

        result: str = self.cursor.execute(
            f"SELECT track_url FROM bgm WHERE member_id='{member_id}'"
        ).fetchone()[0]

        return result

    def fetch_bgm_all(self):

        result = self.cursor.execute("SELECT * FROM bgm").fetchall()
        bgm: dict[str, str] = {}

        for row in result:
            member_id = row[0]
            track_url = row[1]

            bgm[member_id] = track_url

        return bgm

    def __insert_bgm(self, member_id: str, track_url: str):

        self.cursor.execute(
            f"INSERT INTO bgm(member_id,track_url) VALUES('{member_id}','{track_url}')"
        )
        self.conn.commit()

        return

    def __update_bgm(self, member_id: str, track_url: str):

        self.cursor.execute(
            f"UPDATE favs SET track_url='{track_url}' WHERE member_id='{member_id}'"
        )
        self.conn.commit()

        return

    def update_insert_bgm(self, member_id: str, track_url: str):

        bgm_exists = (
            self.cursor.execute(
                f"SELECT member_id FROM favs WHERE member_id='{member_id}'"
            ).fetchone()
            != []
        )

        if bgm_exists:
            self.__update_bgm(member_id, track_url)
        else:
            self.__insert_bgm(member_id, track_url)

        return

    def fetch_fav(self, member: discord.Member):
        member_roles = member.roles
        available_favs: list[str] = self.cursor.execute(
            "SELECT role_id FROM favs"
        ).fetchall()
        fav_ids: list[str] = []
        favs_data = ""
        for fav in available_favs:
            fav_ids.append(fav[0])
        fav_ids.reverse()
        for role in member_roles:
            if str(role.id) in fav_ids:
                favs_data: str = self.cursor.execute(
                    f"SELECT list_data FROM favs WHERE role_id='{role.id}'"
                ).fetchone()[0]

        if favs_data == "":
            # TODO: some error checking here
            logger.error("failed to grab fav list data")
            return

        favs = DictStrTranscoder.decode(favs_data)
        if not favs:
            return

        return favs

    def fetch_fav_all(self):

        result = self.cursor.execute("SELECT * FROM favs").fetchall()
        favs: dict[str, dict[str, str]] = {}

        for row in result:
            member_id = row[0]
            favs_list = DictStrTranscoder.decode(row[1])

            favs[member_id] = favs_list

        return favs

    def delete_fav(self, role_id: str):

        self.cursor.execute(f"DELETE FROM favs WHERE role_id='{role_id}'")
        self.conn.commit()

        return

    def __insert_fav(self, role_id: str, favs: dict[str, str]):

        self.cursor.execute(
            f"INSERT INTO favs(role_id,list_data) VALUES('{role_id}','{DictStrTranscoder.encode(favs)}')"
        )
        self.conn.commit()

        return

    def __update_fav(self, role_id: str, favs: dict[str, str]):

        self.cursor.execute(
            f"UPDATE favs SET list_data='{DictStrTranscoder.encode(favs)}' WHERE role_id='{role_id}'"
        )
        self.conn.commit()

        return

    def update_insert_fav(self, role_id: str, favs: dict[str, str]):

        favs_exist = (
            self.cursor.execute(
                f"SELECT role_id FROM favs WHERE role_id='{role_id}'"
            ).fetchone()
            != []
        )

        if favs_exist:
            self.__update_fav(role_id, favs)
        else:
            self.__insert_fav(role_id, favs)

        return

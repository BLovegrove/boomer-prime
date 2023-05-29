import os

import discord


class guild:
    id = os.environ["GUILD_ID"]


class bot:
    name = os.environ["NAME"]
    id = os.environ["BOT_ID"]
    token = os.environ["BOT_TOKEN"]
    music_channel = os.environ["MUSIC_CHANNEL"]


class style:
    embed_color = discord.Color.blurple()


class lavalink:
    host = os.environ["LAVALINK_IP"]
    port = os.environ["LAVALINK_PORT"]
    password = os.environ["LAVALINK_PASSWORD"]
    region = os.environ["LAVALINK_REGION"]
    name = "default-node"


class player:
    volume_default = (
        os.environ["PLAYER_VOLUME_DEFAULT"]
        if os.environ["PLAYER_VOLUME_DEFAULT"]
        else 50
    )
    volume_idle = (
        os.environ["PLAYER_VOLUME_IDLE"] if os.environ["PLAYER_VOLUME_IDLE"] else 5
    )
    list_len = (
        os.environ["PLAYER_LIST_LENGTH"] if os.environ["PLAYER_LIST_LENGTH"] else 9
    )
    bgm_default = os.environ["PLAYER_BACKGROUND_MUSIC"]

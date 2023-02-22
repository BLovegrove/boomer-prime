import traceback

import discord
import lavalink
from discord.ext import commands

import config as cfg

from ...handlers.database import DBHandler
from ...handlers.voice import VoiceHandler
from ...util.models import LavaBot


class QueueEnd(commands.Cog):
    def __init__(self, bot: LavaBot) -> None:
        self.bot = bot
        self.voice_handler = VoiceHandler(bot)
        self.DatabaseHandler = DBHandler(bot)

    @lavalink.listener(lavalink.events.QueueEndEvent)
    async def on_queue_end(self, event: lavalink.events.QueueEndEvent):
        # TODO: Followup on issue report so theres no need to manually type player.node
        player = self.voice_handler.fetch_player(self.bot)
        if not player:
            return
        await player.set_volume(cfg.player.volume_idle)
        player.node: lavalink.Node = player.node
        result: lavalink.LoadResult = await player.node.get_tracks(
            self.DatabaseHandler.fetch_bgm(player.fetch("summoner_id"))
        )

        if (
            not result
            or not result.tracks
            or result.load_type != result.load_type.TRACK
        ):
            player.queue.clear()
            await self.voice_handler.disconnect(self.bot, player)

            if not player.channel_id:
                logger.warning(f"Failed to find text channel while queuing idle track.")
                return

            channel = self.bot.get_channel(player.channel_id)
            channel.send(
                ":warning: Nothing found when looking for idle music! Look for a new video."
            )

        if player.fetch("idle"):
            player.set_loop(player.LOOP_NONE)
            player.queue.clear()
            await player.skip()

        track = result.tracks[0]
        player.queue.append(track, 0)

        player.store("idle", True)
        player.set_loop(player.LOOP_SINGLE)

        if not player.is_playing:
            await player.play()


async def setup(bot: LavaBot):
    await bot.add_cog(QueueEnd(bot))

import discord
import lavalink
from discord.ext import commands

import config as cfg

from ...handlers.voice import VoiceHandler
from ...util.models import LavaBot


class QueueEnd(commands.Cog):
    def __init__(self, bot: LavaBot) -> None:
        super().__init__(bot)

        self.bot = bot
        self.voice_handler = VoiceHandler(bot)
        self.player = self.voice_handler.fetch_player(bot)
        if not self.player:
            return

        self.bot.lavalink.add_event_hook()

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            await self.player.set_volume(cfg.player.volume_idle)

            # TODO: Followup on issue report so theres no need to manually type player.node
            self.player.node: lavalink.Node = self.player.node
            # TODO: Add database support for idle tracks
            result: lavalink.LoadResult = await self.player.node.get_tracks()


async def setup(bot: LavaBot):
    await bot.add_cog(QueueEnd(bot))

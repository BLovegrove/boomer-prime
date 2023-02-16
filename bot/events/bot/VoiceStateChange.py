import discord
from discord.ext import commands

from ...handlers.voice import VoiceHandler
from ...util.models import LavaBot


class VoiceStateChange(commands.Cog):
    def __init__(self, bot: LavaBot) -> None:
        super().__init__(bot)

        self.bot = bot
        self.voice_handler = VoiceHandler(bot)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        
        player = self.voice_handler.fetch_player(self.bot)
        if not player:
            return

        if (
            after.channel.id == player.channel_id
            or before.channel.id != player.channel_id
            or not before.channel
            or after.channel
        ):
            return

        channel = self.bot.get_channel(player.channel_id)
        if not channel:
            return

        if channel.member_count == 1:
            self.voice_handler.disconnect()


async def setup(bot: LavaBot):
    await bot.add_cog(VoiceStateChange(bot))

import discord
import lavalink
from discord import app_commands
from discord.ext import commands

import config as cfg

from ...handlers.music import MusicHandler
from ...handlers.voice import VoiceHandler
from ...util.models import LavaBot


class Template(commands.Cog):
    def __init__(self, bot: LavaBot) -> None:
        self.bot = bot
        self.music_handler = MusicHandler(bot)
        self.voice_handler = VoiceHandler(bot)

    @app_commands.command(
        description=f"Summons {cfg.bot.name} to your voice channel and plays the summoners idle tune."
    )
    async def ok(self, interaction: discord.Interaction):
        await interaction.response.defer()
        player = await self.voice_handler.ensure_voice(interaction)

        await interaction.edit_original_response(
            content=f"Joined <#{interaction.user.voice.channel.id}>"
        )
        await player.set_volume(cfg.player.volume_default)
        player.store("summoner_id", interaction.user.id)
        await self.bot.lavalink._dispatch_event(lavalink.events.QueueEndEvent(player))
        return


async def setup(bot: LavaBot):
    await bot.add_cog(Template(bot))

import discord
from discord import app_commands
from discord.ext import commands

from ...handlers.embeds import ListEmbedBuilder
from ...handlers.music import MusicHandler
from ...handlers.voice import VoiceHandler
from ...util.models import LavaBot


class List(commands.Cog):
    def __init__(self, bot: LavaBot) -> None:
        self.bot = bot
        self.music_handler = MusicHandler(bot)
        self.voice_handler = VoiceHandler(bot)

    @app_commands.command(
        description="Displays an interactive queue listing! Click the buttons to cycle through pages."
    )
    @app_commands.describe(
        page="Page of the queue you want to list off. If you're unsure, just leave this blank."
    )
    async def list(self, interaction: discord.Interaction, page: int = None):

        player = await self.voice_handler.ensure_voice(interaction)
        embed = ListEmbedBuilder(player, page if page != None else 1)
        await interaction.response.send_message(embed=embed.construct())

        return


async def setup(bot: LavaBot):
    await bot.add_cog(List(bot))

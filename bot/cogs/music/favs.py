import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View

from ...handlers.database import DBHandler
from ...handlers.embeds import FavsEmbedBuilder
from ...handlers.music import MusicHandler
from ...handlers.voice import VoiceHandler
from ...util.models import LavaBot


class Favs(commands.Cog):
    def __init__(self, bot: LavaBot) -> None:
        self.bot = bot
        self.music_handler = MusicHandler(bot)
        self.voice_handler = VoiceHandler(bot)
        self.database_handler = DBHandler(bot)

    group = app_commands.Group(
        name="favs", description="Queue up and manage some of your favorite tunes!"
    )

    @group.command(
        description="Show a list of all the favorites for your group. Play them from the list directly!"
    )
    async def list(self, interaction: discord.Interaction):
        await interaction.response.defer()

        role, favs = self.database_handler.fetch_favs(interaction.user)

        if not role:
            await interaction.response.edit_message(
                content="None of your roles support a favs list! If you think this is a mistake, ping your friendly neighborhood admin."
            )
            return
        # favs_names = [
        #     list(favs.keys())[i : i + 3] for i in range(0, len(list(favs.keys())), 3)
        # ]
        # favs_tracks = [
        #     list(favs.values())[i : i + 3]
        #     for i in range(0, len(list(favs.values())), 3)
        # ]

        # view = View(timeout=120)

        # for row in favs_names:
        #     for name in row:
        # row_index = favs_names.index(row)
        # col_index = row.index(name)

        # view.add_item(
        #     Button(
        #         style=discord.ButtonStyle.primary,
        #         custom_id=name,
        #         label=name,
        #         emoji="❌",
        #         row=row_index,
        #     )
        # )

        await interaction.followup.send(
            content="List found!", embed=FavsEmbedBuilder(role, favs).construct()
        )

        return

    async def play_autocomplete(self, interaction: discord.Interaction, current: str):
        data = []
        role_id, favs = self.database_handler.fetch_favs(interaction.user)
        if not favs:
            favs = ["404_no_favslist"]

        for fav in list(favs.keys()):
            if current.lower() in fav.lower():
                data.append(app_commands.Choice(name=fav, value=favs[fav]))

        return data

    @group.command(description="Play a specific favourite")
    @app_commands.autocomplete(fav=play_autocomplete)
    async def play(self, interaction: discord.Interaction, fav: str):
        await self.music_handler.play(interaction, fav)


async def setup(bot: LavaBot):
    await bot.add_cog(Favs(bot))

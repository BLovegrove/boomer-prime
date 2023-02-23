import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from loguru import logger

import config as cfg

from ...handlers.database import DBHandler
from ...handlers.voice import VoiceHandler
from ...util.models import LavaBot


class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: LavaBot = bot
        self.database_handler = DBHandler(bot)

    @app_commands.command(
        name="dev",
        description=f"Runs a series of dev commands for testing and maintenance purposes.",
    )
    @app_commands.choices(
        command=[
            Choice(name="Kill bot", value="die"),
            Choice(name="Ping test", value="ping"),
            Choice(name="Fetch player object", value="fetchplayer"),
        ]
    )
    async def dev(self, interaction: discord.Interaction, command: Choice[str]):
        match command.value:
            case "die":
                await interaction.response.send_message(
                    f"Restarting the bot. Please wait until {cfg.bot.name} has the 'Online' or 'Idle' status icon before doing any more commands."
                )
                self.database_handler.close()
                player = self.bot.lavalink.player_manager.get(interaction.guild_id)
                if player:
                    handler = VoiceHandler(self.bot)
                    await handler.disconnect(self.bot, player)
                await self.bot.close()
                return
            case "ping":
                await interaction.response.send_message(
                    f"Pong! ({self.bot.ws.VOICE_PING})"
                )
                return
            case "fetchplayer":
                await interaction.response.defer(ephemeral=True)
                handler = VoiceHandler(self.bot)
                player = handler.fetch_player(self.bot)
                logger.debug(f"Player: {player}")
                logger.debug(f"Player guild: {player.guild_id}")
                logger.debug(f"Player VC: {player.channel_id}")
                await interaction.edit_original_response(
                    content="Dev command completed"
                )
                return
            case "default":
                await interaction.response.send_message(
                    "Dev comamnd failed. Couldn't find a subcommand matching your input.",
                    ephemeral=True,
                )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dev(bot))

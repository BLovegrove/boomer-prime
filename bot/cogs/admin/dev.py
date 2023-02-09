import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands


import config as cfg


class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="die",
        description=f"Runs a series of dev commands for testing and maintenance purposes.",
    )
    @app_commands.choices(
        command=[
            Choice(name="Kill bot", value="die"),
            Choice(name="Ping test", value="ping"),
        ]
    )
    async def execute(self, interaction: discord.Interaction, command: Choice[str]):
        match command.name:
            case "die":
                await interaction.response.send_message(
                    f"Restarting the bot. Please wait until {cfg.bot.name} has the 'Online' status icon before doign any more commands."
                )
                await self.bot.close()
                return
            case "ping":
                await interaction.response.send_message(
                    f"Pong! ({self.bot.ws.VOICE_PING})"
                )
                return
            case "default":
                await interaction.response.send_message(
                    "Dev comamnd failed. Couldn't find a subcommand matching your input.",
                    ephemeral=True,
                )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dev(bot))

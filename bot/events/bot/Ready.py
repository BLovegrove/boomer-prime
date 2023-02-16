import discord
from discord.ext import commands

import config as cfg

from ...util.models import LavaBot


class Ready(commands.Cog):
    def __init__(self, bot: LavaBot) -> None:
        super().__init__(bot)
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(f"Bot is logged in as {self.bot.user}")
        self.bot.logger.info("Syncing slash commands...")
        try:
            guild_obj = discord.Object(id=cfg.guild.id)
            self.bot.tree.copy_global_to(guild=guild_obj)
            synced = await self.bot.tree.sync(guild=guild_obj)
            self.bot.logger.info(f"Synced {len(synced)} commands.")
        except Exception as e:
            self.bot.logger.error(e)


async def setup(bot: LavaBot):
    await bot.add_cog(Ready(bot))

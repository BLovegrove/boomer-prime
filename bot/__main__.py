import config as cfg

from .util import helper, models

logger = helper.logs.getLogger()

# class Bot(commands.Bot):
#     def __init__(self) -> None:
#         super().__init__(
#             command_prefix=commands.when_mentioned, intents=discord.Intents.all()
#         )
#         self.cogList = helper.cogs.search()

#     # Cog loading
#     async def setup_hook(self) -> None:
#         for extension in self.cogList:
#             await self.load_extension(extension)
#         return await super().setup_hook()

#     # On-ready for command syncing, bootup messages, etc.
#     async def on_ready(self):
#         logger.info(f"Bot is logged in as {self.user}")
#         logger.info("Syncing slash commands...")
#         try:
#             guild_obj = discord.Object(id=cfg.guild.id)
#             self.tree.copy_global_to(guild=guild_obj)
#             synced = await self.tree.sync(guild=guild_obj)
#             logger.info(f"Synced {len(synced)} commands.")
#         except Exception as e:
#             logger.error(e)


# make sure the main py file is being run as a file and not imported
def main():
    bot = models.LavaBot()
    bot.run(cfg.bot.token)
    bot.update_lavalink()


if __name__ == "__main__":
    main()

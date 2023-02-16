import discord
import lavalink

import config as cfg

from ..util import models


class VoiceHandler:
    def __init__(self, bot: models.LavaBot) -> None:
        self.bot = bot

    def fetch_player(self, bot: models.LavaBot) -> lavalink.DefaultPlayer:
        return bot.lavalink.player_manager.get(cfg.guild.id)

    async def ensure_voice(self, interaction: discord.Interaction):

        # ---------------------------------- guards ---------------------------------- #
        # sender validation: in guild
        if (
            (not interaction.guild.get_member(interaction.user.id))
            or (not interaction.guild)
            or (interaction.channel)
        ):
            await interaction.response.send_message(
                "Try sending this within a valid server.", ephemeral=True
            )
            return

        # sender validation: in voice
        if not interaction.user.voice.channel:
            await interaction.response.send_message(
                "You need to join a voice channel.", ephemeral=True
            )
            return

        # bot validation: connected to VC
        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.create(
            interaction.guild.id
        )
        if not player.channel_id:
            await interaction.response.send_message(
                f"Can't do anything unless the bot is connected! Try /ok {cfg.bot.name} or /play first!",
                ephemeral=True,
            )
            return

        # sender validation: share common VC with bot
        if player.channel_id != interaction.user.voice.channel.id:
            await interaction.response.send_message(
                f"{cfg.bot.name} is already in <#{player.channel_id}> :rolling_eyes:"
            )
            await interaction.followup.send(
                "The bot can't be in two palces at once - join the linked channel to use them.",
                ephemeral=True,
            )
            return

        # --------------------- end guards, run success condition -------------------- #

        self.bot.player_exists = True
        return player

    async def disconnect(self, bot: models.LavaBot, player: lavalink.DefaultPlayer):
        player.queue.clear()
        await player.stop()
        player.set_repeat(False)
        player.store("track_repeat", False)
        await player.set_volume(cfg.player.volume_default)
        await player.clear_filters()
        await player.destroy()
        await self.update_status(bot, player)

    async def update_status(self, bot: models.LavaBot, player: lavalink.DefaultPlayer):
        suffix = ""

        # add modifiers to suffix
        if player.fetch("track_repeat"):
            suffix = " (on repeat)"

        if player.is_playing:
            await bot.change_presence(
                activity=discord.Activity(
                    name=f"{player.current.title + suffix}",
                    type=discord.ActivityType.listening,
                ),
                status=discord.Status.online,
            )

        else:
            await bot.change_presence(
                activity=discord.Activity(
                    name="nothing.", type=discord.ActivityType.listening
                ),
                status=discord.Status.idle,
            )

        bot.logger.info(f"Updated activity info to: {bot.activity}")
        bot.logger.info(f"Updated status info to: {bot.status}")
        return

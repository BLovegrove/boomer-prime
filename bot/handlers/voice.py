import discord
import lavalink

import config as cfg

from ..util import models


class VoiceHandler:
    def __init__(self, bot: models.LavaBot) -> None:
        self.bot = bot

    def fetch_player(self, bot: models.LavaBot) -> lavalink.DefaultPlayer:
        try:
            player = bot.lavalink.player_manager.get(cfg.guild.id)
            return player
        except Exception as e:
            self.bot.logger.warn("Failed to fetch player")
            return

    async def ensure_voice(self, interaction: discord.Interaction):

        player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(
            interaction.guild_id
        )
        if not player:
            return

        # ---------------------------------- guards ---------------------------------- #
        # sender validation: in guild
        if (
            (not interaction.guild.get_member(interaction.user.id))
            or (not interaction.guild)
            or (not interaction.channel)
        ):
            await interaction.response.send_message(
                "Try sending this within a valid server.", ephemeral=True
            )
            self.bot.logger.error(
                f"Failed to find guild member in interaction for VoiceHandler command. NOT_MEMBER:{not interaction.guild.get_member(interaction.user.id)}, OUTSIDE_GUILD:{not interaction.guild}, WITHIN_CHANNEL:{not interaction.channel}"
            )
            return

        # sender validation: in voice
        if not interaction.user.voice:
            await interaction.response.send_message(
                "You need to join a voice channel.", ephemeral=True
            )
            return

        # bot validation: connected to VC

        # player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.create(
        #     interaction.guild.id
        # )

        if not player.is_connected:
            player.store("pages", 0)
            player.store("idle", False)
            await interaction.user.voice.channel.connect(cls=models.LavalinkVoiceClient)

        elif player.channel_id != interaction.user.voice.channel.id:
            self.bot.logger.warn(
                f"Bot is already in a channel. Failed to move the bot. PLAYER_CHANNEL:{player.channel_id}, MEMBER_CHANNEL:{interaction.user.voice.channel.id}"
            )
            await interaction.response.send_message(
                f"{cfg.bot.name} is already in <#{player.channel_id}> :rolling_eyes:"
            )
            await interaction.followup.send(
                "The bot can't be in two places at once - join the linked channel to use them.",
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

    async def update_status(
        self, bot: models.LavaBot, player: lavalink.DefaultPlayer = None
    ):
        suffix = ""

        if player and player.fetch("track_repeat"):
            suffix = " (on repeat)"

        activity = None
        status = None

        if player and player.is_playing:
            activity = discord.Activity(
                name=f"{player.current.title + suffix}",
                type=discord.ActivityType.listening,
            )
            status = discord.Status.online
            await bot.change_presence(activity=activity, status=status)

        else:
            activity = discord.Activity(
                name="nothing.", type=discord.ActivityType.listening
            )
            status = discord.Status.idle
            await bot.change_presence(activity=activity, status=status)

        bot.logger.info(f"Updated activity info to: {activity.name}")
        bot.logger.info(f"Updated status info to: {status}")
        return

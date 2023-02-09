import discord
import lavalink
from discord.ext import commands

import config as cfg

from . import helper


class LavaBot(commands.Bot):
    """
    Standard discord.ext.commands.Bot with added lavalink attribute + type for intellisense
    logger also included as self.logger
    """

    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned, intents=discord.Intents.all()
        )
        self.cogList = helper.cogs.search()
        self.lavalink = lavalink.Client(self.user.id)
        self.logger = helper.logs.getLogger()
        self.player_exists = False

    # Cog loading
    async def setup_hook(self) -> None:
        for extension in self.cogList:
            await self.load_extension(extension)
        return await super().setup_hook()

    # On-ready for command syncing, bootup messages, etc.
    async def on_ready(self):
        self.logger.info(f"Bot is logged in as {self.user}")
        self.logger.info("Syncing slash commands...")
        try:
            guild_obj = discord.Object(id=cfg.guild.id)
            self.tree.copy_global_to(guild=guild_obj)
            synced = await self.tree.sync(guild=guild_obj)
            self.logger.info(f"Synced {len(synced)} commands.")
        except Exception as e:
            self.logger.error(e)


class LavalinkVoiceClient(discord.VoiceClient):
    """
    This is the preferred way to handle external voice sending
    This client will be created via a cls in the connect method of the channel
    see the following documentation:
    https://discordpy.readthedocs.io/en/latest/api.html#voiceprotocol"""

    def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
        super().__init__(client, channel)
        self.client = client
        self.channel = channel
        # ensure a client already exists
        if hasattr(self.client, "lavalink"):
            self.lavalink: lavalink.Client = self.client.lavalink
        else:
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(  # type: ignore
                cfg.lavalink.host,
                cfg.lavalink.port,
                cfg.lavalink.password,
                "us",
                "default-node",
            )
            self.lavalink: lavalink.Client = self.client.lavalink

    async def on_voice_server_update(self, data):
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {"t": "VOICE_SERVER_UPDATE", "d": data}
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {"t": "VOICE_STATE_UPDATE", "d": data}
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(
        self,
        *,
        timeout: float,
        reconnect: bool,
        self_deaf: bool = True,
        self_mute: bool = False,
    ) -> None:
        """
        Connect the bot to the voice channel and create a player_manager
        if it doesn't exist yet.
        """
        # ensure there is a player_manager when creating a new voice_client
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(
            channel=self.channel, self_mute=self_mute, self_deaf=self_deaf
        )

    async def disconnect(self, *, force: bool = False) -> None:
        """
        Handles the disconnect.
        Cleans up running player and leaves the voice client.
        """
        player: lavalink.DefaultPlayer = self.lavalink.player_manager.get(
            self.channel.guild.id
        )

        # no need to disconnect if we are not connected
        if not force and not player.is_connected:
            return

        # None means disconnect
        await self.channel.guild.change_voice_state(channel=None)

        # update the channel_id of the player to None
        # this must be done because the on_voice_state_update that would set channel_id
        # to None doesn't get dispatched after the disconnect
        player.channel_id = None
        self.cleanup()

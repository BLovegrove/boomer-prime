import discord
import lavalink

import config as cfg

from ..handlers import embeds, queue, voice
from ..util import models


class MusicHandler:
    def __init__(self, bot: models.LavaBot) -> None:
        self.bot = bot
        self.voice_handler = voice.VoiceHandler(self.bot)
        self.queue_handler = queue.QueueHandler(self.bot, self.voice_handler)

    async def __add_track(
        self,
        interaction: discord.Interaction,
        player: lavalink.DefaultPlayer,
        track: lavalink.AudioTrack = None,
        tracks: list[lavalink.AudioTrack] = None,
        result: lavalink.LoadResult = None,
    ):
        embed = discord.Embed()

        if track:
            embed = embeds.TrackEmbedBuilder(interaction, track, player).construct()
            player.add(track)
            self.bot.logger.info(f"Track added to queue: {track.title}")

        elif tracks and result:
            embed = embeds.PlaylistEmbedBuilder(interaction, result, player).construct()

            for track in tracks:
                player.add(track)

            self.bot.logger.info(f"Playlist added to queue.")

        if player.fetch("idle"):
            player.store("idle", False)
            player.set_loop(player.LOOP_NONE)
            await player.set_volume(cfg.player.volume_default)
            await player.skip()

        elif not player.is_playing:
            await player.set_volume(cfg.player.volume_default)
            await player.play()

        await interaction.response.edit_message(embed=embed)

    async def play(self, interaction: discord.Interaction, search: str):
        player = await self.voice_handler.ensure_voice(interaction)
        if not player:
            return

        self.bot.logger.info(f"Attempting to play song... Query: {search}")

        await interaction.response.defer()

        # TODO: Followup on issue report so theres no need to manually type player.node
        player.node: lavalink.Node = player.node
        result: lavalink.LoadResult = await player.node.get_tracks(search)

        try:

            match result.load_type:
                case "LOAD_FAILED":
                    await interaction.response.edit_message(
                        content="Failed to load track, please use a different URL or different search term."
                    )

                case "NO_MATCHES":
                    await interaction.response.edit_message(
                        content="404 song not found! Try something else."
                    )

                case "SEARCH_RESULT" | "TRACK_LOADED":
                    track = result.tracks[0]
                    await self.__add_track(interaction, player, track)

                case "PLAYLIST_LOADED":
                    tracks = result.tracks
                    await self.__add_track(interaction, player, None, tracks, result)

                case _:
                    await interaction.response.edit_message(
                        content="Something unexpected happened. Contact your server owner or local bot dev(s) immediately and let them know the exact command you tried to run."
                    )
                    self.bot.logger.warn(
                        f"Load type for play request defaulted. Query '{search}' result as follows:"
                    )
                    self.bot.logger.warn(result)

        except Exception as e:
            self.bot.logger.error(e)
            return

        self.queue_handler.update_pages(player)

        return

    async def skip(
        self, interaction: discord.Interaction, index: int, trim_queue: bool = True
    ):
        if not self.bot.player_exists:
            await interaction.response.send_message(
                f":warning: There is no player running. Play a song or invite {cfg.bot.name} to a VC first."
            )
            return

        player = await self.voice_handler.ensure_voice(interaction)
        if not player:
            return

        if len(player.queue) == 0 and player.loop != player.LOOP_SINGLE:
            await interaction.response.send_message(
                ":notepad_spiral: End of queue - tie for your daily dose of idle tunes!"
            )
            await player.skip()
            return

        if player.loop == player.LOOP_SINGLE:
            next_track = player.current

            if not next_track:
                await interaction.response.send_message(
                    f"Error! Track not found. Somethign went wrong with playback - try kicking {cfg.bot.name} from the VC and trying again."
                )
                return

            embed = embeds.SkipEmbedBuilder(interaction, next_track, player, 0)
            await interaction.response.send_message(
                ":repeat_one: Repeat enabled - looping song.",
                embed=embed.construct(),
            )
            await player.seek(0)
            self.bot.logger.info("Skipped song (repeat enabled).")
            return

        if index < 0:
            await interaction.response.send_message(
                ":warning: That index is too low! Queue starts at #1.", ephemeral=True
            )
            self.bot.logger.warn(
                f"Skip failed. Index too low (expected: >=1. Recieved: {index})"
            )
            return

        elif index > len(player.queue):
            await interaction.response.send_message(
                f":warning: That index is too high! Queue only {len(player.queue)} items long.",
                ephemeral=True,
            )
            self.bot.logger.warn(
                f"Skip failed. Index too high (expected: <={len(player.queue)}. Recieved: {index})"
            )
            return

        else:
            if trim_queue:
                self.bot.logger.info(
                    f"Skipped queue to track {index} of {len(player.queue) + 1}"
                )

                if index - 1 != 0:
                    # TODO: confirm this works how I think it does...
                    player.queue = player.queue[: index + 1]
                    return

            else:
                self.bot.logger.info(
                    f"Jumped to track {index} of {len(player.queue)} in queue."
                )
                jump_track = player.queue.pop(index - 1)

                if not jump_track:
                    await interaction.response.send_message("Error! Track not found.")
                    return

                player.add(jump_track, index=0)

            next_track = player.queue[0]
            if isinstance(next_track, lavalink.DeferredAudioTrack):
                next_track = await next_track.load(self.bot.lavalink)
                try:
                    next_track = lavalink.decode_track(next_track)

                except Exception as e:
                    self.bot.logger.error(e)

            if not next_track:
                await interaction.response.send_message("Error! Track not found.")
                return

            await player.skip()
            self.bot.logger.info("Skipping current track...")

            embed = embeds.SkipEmbedBuilder(interaction, next_track, player, index)
            await interaction.response.send_message(embed=embed.construct())

            self.queue_handler.update_pages(player)
            await self.voice_handler.update_status(self.bot, player)

            return
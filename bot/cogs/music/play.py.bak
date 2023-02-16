import discord
from discord import app_commands
from discord.ext import commands

import config as cfg

from ...util import models


class play(models.LavaBot):
    def __init__(self, bot: models.LavaBot) -> None:
        self.bot = bot

    @app_commands.Command(
        name="play",
        description=f"Plays music! Summons {cfg.bot.name} if they aren't running and adds a song to the queue if they are.",
    )
    @app_commands.describe(search="The name/artist/url of the song you want to find")
    async def play(self, interaction: discord.Interaction, search: str):

        # Get the player for this guild from cache.
        player = self.bot.lavalink.player_manager.get(interaction.guild.id)
        # Remove leading and trailing <>. <> may be used to suppress embedding links in Discord.
        search = search.strip("<>")

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not url_rx.match(search):
            search = f"ytsearch:{search}"

        # Get the results for the query from Lavalink.
        results = await player.node.get_tracks(search)

        # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
        # Alternatively, results.tracks could be an empty array if the query yielded no tracks.
        if not results or not results.tracks:
            return await ctx.send("Nothing found!")

        embed = discord.Embed(color=discord.Color.blurple())

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if results.load_type == "PLAYLIST_LOADED":
            tracks = results.tracks

            for track in tracks:
                # Add all of the tracks from the playlist to the queue.
                player.add(requester=ctx.author.id, track=track)

            embed.title = "Playlist Enqueued!"
            embed.description = f"{results.playlist_info.name} - {len(tracks)} tracks"
        else:
            track = results.tracks[0]
            embed.title = "Track Enqueued"
            embed.description = f"[{track.title}]({track.uri})"

            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip
        # the current track.
        if not player.is_playing:
            await player.play()

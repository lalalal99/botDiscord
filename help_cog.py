from datetime import datetime

import discord
import pytz
from discord.ext import commands

from globals import getHoursMinutes


class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
General commands:
mhelp - displays all the available commands
mp <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current song if it was paused
mq - displays the current music queue
mskip - skips the current song being played
mclear - Stops the music and clears the queue
mleave - Disconnected the bot from the voice channel
mpause - pauses the current song being played or resumes if already paused
mresume - resumes playing the current song
```
"""
        self.text_channel_list = []

    # some debug info so that we know the bot has started
    @commands.Cog.listener()
    async def on_ready(self):
        # for guild in self.bot.guilds:
        #     for channel in guild.text_channels:
        #         self.text_channel_list.append(channel)

        # await self.send_to_all(self.help_message)
        print(f"[{getHoursMinutes()}][service] Bot ready!")

    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)

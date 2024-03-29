import asyncio
import os
from datetime import datetime

import discord
import pytz
from discord.ext import commands

from globals import getHoursMinutes
from help_cog import help_cog
from music_cog import music_cog
from servers_cog import servers_cog

# from test_cog import test_cog

GUILD = discord.Object(id=558367979931172870)

bot = commands.Bot(command_prefix='m', intents=discord.Intents.all())

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def setup():
    await bot.add_cog(music_cog(bot))
    await bot.add_cog(servers_cog(bot))
    # await bot.add_cog(test_cog(bot))

    @bot.event
    async def on_ready():
        print(f"[{getHoursMinutes()}][service] Bot ready!")
        bot.tree.copy_global_to(guild=GUILD)
        await bot.tree.sync(guild=GUILD)

asyncio.run(setup())
bot.run(os.getenv("DISCORD_TOKEN"))

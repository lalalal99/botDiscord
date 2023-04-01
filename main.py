import asyncio
import os

import discord
from discord.ext import commands

# import all of the cogs
from help_cog import help_cog
from music_cog import music_cog
from servers_cog import servers_cog

# from test_cog import test_cog

bot = commands.Bot(command_prefix='m', intents=discord.Intents.all())

# remove the default help command so that we can write out own
bot.remove_command('help')

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def setup():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))
    await bot.add_cog(servers_cog(bot))
    # await bot.add_cog(test_cog(bot))

asyncio.run(setup())
# start the bot with our token
bot.run(os.getenv("DISCORD_TOKEN"))

import discord
from discord.ext import commands
from discord import app_commands
from typing import List

mycolors = ["red", "white", "yellow"]

# intents = discord.Intents.default()
# client = discord.Client(intents=intents)
# tree = app_commands.CommandTree(client)


class test_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot.user

    # @app_commands.command()
    # async def fruits(self, interaction: discord.Interaction, fruit: str):
    #     await interaction.response.send_message(f'Your favourite fruit seems to be {fruit}')

    # @fruits.autocomplete('fruit')
    # async def fruits_autocomplete(self,
    #                               interaction: discord.Interaction,
    #                               current: str,
    #                               ) -> List[app_commands.Choice[str]]:
    #     fruits = ['Banana', 'Pineapple', 'Apple',
    #               'Watermelon', 'Melon', 'Cherry']
    #     return [
    #         app_commands.Choice(name=fruit, value=fruit)
    #         for fruit in fruits if current.lower() in fruit.lower()
    #     ]

    # @app_commands.command()
    @cog_ext.cog_slash(name="ping")
    async def ping(self, ctx:SlashContext) -> None:
        ping1 = f"{str(round(self.client.latency * 1000))} ms"
        embed = discord.Embed(
            title="**Pong!**", description="**" + ping1 + "**", color=0xafdafc)
        await interaction.response.send_message(embed=embed)

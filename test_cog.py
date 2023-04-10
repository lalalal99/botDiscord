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

    # @ commands.Cog.listener()
    # async def on_ready(self):
    #     await self.bot.tree.sync()
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
    # @ commands.Cog.hybrid_command()
    # async def ping(self, ctx) -> None:
    #     ping1 = f"{str(round(self.client.latency * 1000))} ms"
    #     embed = discord.Embed(
    #         title="**Pong!**", description="**" + ping1 + "**", color=0xafdafc)
    #     await ctx.send(embed=embed)

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx, a=3) -> None:
        ping1 = f"ms"
        embed = discord.Embed(
            title="**Pong!**", description="**" + ping1 + "**", color=0xafdafc)
        await ctx.send(embed=embed)

    @ping.autocomplete("a")
    async def ping_autocomplete(self,
                                interaction: discord.Interaction,
                                current: str,
                                ) -> List[app_commands.Choice[str]]:
        return 0


    # @commands.hybrid_command(name="top", help="Plays top songs from spotify")
    # async def top(self, ctx, genre, n):
    #     if not ctx.author.voice:
    #         await ctx.send("Connect to a voice channel!")
    #         return

    #     voice_channel = ctx.author.voice.channel
    #     noshuffle = False
    #     cmds = {"-"+genre for genre in pl_id.keys()}
    #     args = set(args)

    #     if "-ns" in args:
    #         noshuffle = True
    #         args.remove("-ns")
    #     try:
    #         genre = args.intersection(cmds).pop()
    #         args.remove(genre)
    #     except:
    #         genre = "-default"

    #     chart = get_chart(genre[1:])

    #     try:
    #         maxsongs = args.pop()
    #     except:
    #         maxsongs = None

    #     if maxsongs:
    #         if not maxsongs.isnumeric():
    #             print(
    #                 f"[{getHoursMinutes()}][service:error] Argument is not a number")
    #             await ctx.send(f"[{getHoursMinutes()}][service:error] Argument is not a number")
    #             return
    #         maxsongs = int(maxsongs)
    #     else:
    #         maxsongs = 10

    #     if len(chart) < maxsongs:
    #         maxsongs = len(chart)

    #     if not noshuffle:
    #         random.shuffle(chart)

    #     await ctx.send(str(maxsongs) + (" songs " if maxsongs > 1 else " song ") + "added to the queue!")

    #     songs = [None] * maxsongs

    #     async def async_yt_search(query, i):
    #         song = await self.search_yt(query)
    #         songs[i] = [song, voice_channel]

    #     def wrap_async_func(query, i):
    #         asyncio.run(async_yt_search(query, i))

    #     query = chart[0]["Artist"] + " " + chart[0]["TrackName"] + " lyrics"
    #     await self.play(ctx, query + " -nv")
    #     print(1, "-", query)

    #     threads = []
    #     for i in range(1,  maxsongs):
    #         query = chart[i]["Artist"] + " " + \
    #             chart[i]["TrackName"] + " lyrics"
    #         print(i+1, "-", query)

    #         _t = threading.Thread(target=wrap_async_func, args=(query, i))
    #         threads.append(_t)

    #     for t in threads:
    #         await asyncio.sleep(0.1)
    #         t.start()

    #     for t_ in threads:
    #         t_.join()

    #     print("All songs downloaded.")

    #     for song in songs[1:]:
    #         self.music_queue.append(song)

    #     self.top_playing = True

    # @top.autocomplete("genre")
    # async def top_autocomplete(self,
    #                            interaction: discord.Interaction,
    #                            current: str,
    #                            ) -> typing.List[app_commands.Choice[str]]:
    #     return [app_commands.Choice(name=genre, value=genre)
    #             for genre in pl_id.keys()]

    # @top.autocomplete("n")
    # async def top_autocomplete(self,
    #                            interaction: discord.Interaction,
    #                            current: str,
    #                            ) -> typing.List[app_commands.Choice[str]]:
    #     return [app_commands.Choice(name=x, value=x)
    #             for x in range(1, 11)]
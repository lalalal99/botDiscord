import asyncio
import random
import threading
import time
import typing
from datetime import datetime
from pprint import pprint

import discord
import pytz
from discord import app_commands
from discord.ext import commands, tasks
from tabulate import tabulate
from yt_dlp import YoutubeDL

from globals import *
from spotify_top_songs import get_chart, pl_id


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timer = 0

        # all the music related stuff
        self.is_playing = False
        self.is_paused = False
        self.looping = False
        self.now_playing = ""
        self.top_playing = False
        self.is_radio_playing = False
        self.loop_queue = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {"quiet": True,
                            'format': 'bestaudio',
                            'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'}

        self.vc = None

    @ tasks.loop(seconds=5)
    async def status_task(self):
        if self.vc != None:
            if self.music_queue or self.vc.is_playing():
                self.timer = time.time()
                return

            current_time = time.time()
            if current_time - self.timer >= (3 * 60):
                if self.vc.is_connected():
                    print(
                        f"[{getHoursMinutes()}][service] Bot disconnected due to inactivity")
                    await self.dc(None)

    @ commands.Cog.listener()
    async def on_ready(self):
        self.timer = time.time()
        self.status_task.start()

    # searching the item on youtube
    async def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" %
                                        item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['url'], 'title': info['title']}

    @commands.command(name="play", aliases=["p", "playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        if self.is_radio_playing:
            self.vc.stop()
            await self.clear(ctx)

        query = " ".join(args)
        if not ctx.author.voice:
            await ctx.send("Connect to a voice channel!")
            return

        voice_channel = ctx.author.voice.channel

        self.timer = time.time()
        song = await self.search_yt(query)
        if type(song) == type(True):
            await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            return

        if not query.endswith("-nv"):
            await ctx.send(song["title"] + " added to the queue")

        item = [song, voice_channel]
        if self.top_playing:
            self.music_queue.insert(0, item)
        else:
            self.music_queue.append(item)

        if self.is_playing:
            return

        self.is_playing = True
        m_url = self.music_queue[0][0]['source']

        if not self.vc or not self.vc.is_connected():
            self.vc = await self.music_queue[0][1].connect()
            if not self.vc:
                await ctx.send("Could not connect to the voice channel")
                return

        self.now_playing = self.music_queue[0][0]['title']
        self.vc.play(discord.FFmpegPCMAudio(
            m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

    def play_next(self):
        if self.vc == None or not self.vc.is_connected():
            return

        if len(self.music_queue) > 0:
            self.is_playing = True
            if not self.looping:
                # remove the first element as you are currently playing it
                item = self.music_queue.pop(0)
                if self.loop_queue:
                    self.music_queue.append(item)
                if len(self.music_queue) == 0:
                    setToFalse(self, ['is_playing', 'top_playing'])
                    return
            # get the first url
            m_url = self.music_queue[0][0]['source']
            self.now_playing = self.music_queue[0][0]['title']
            self.vc.play(discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            setToFalse(self, ['is_playing',
                              'top_playing',
                              'loop_queue',
                              'loop'])

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()

    @commands.command(name="resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()

    @commands.command(name="loop", help="Toggles loop mode")
    async def loop(self, ctx):
        if self.looping:
            await ctx.send("Looping removed")
        else:
            await ctx.send("Now looping the current track")

        self.looping = not self.looping
        print(f"[service] Looping {self.looping}")

    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        max = 10
        for i in range(0, len(self.music_queue)):
            # display a max of 'max' songs in the current queue
            if (i > max):
                break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
            if max < len(self.music_queue):
                await ctx.send(f"\nAnd {len(self.music_queue) - max} more")
        else:
            await ctx.send("No music in queue")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        self.top_playing = False
        await ctx.send("Music queue cleared")

    @commands.command(name="leave", aliases=["disconnect", "l", "d", "dc"], help="Kicks the bot from VC")
    async def dc(self, ctx):
        setToFalse(self, [
            'is_playing',
            'is_paused',
            'looping',
            'loop_queue',
            'top_playing',
            'is_radio_playing'])
        self.music_queue = []
        self.now_playing = ""
        await self.vc.disconnect()

    @commands.command(name="top", help="Plays top songs from spotify")
    async def top(self, ctx, *args):
        async def async_yt_search(query, i):
            song = await self.search_yt(query)
            songs[i] = [song, voice_channel]

        def wrap_async_func(query, i):
            asyncio.run(async_yt_search(query, i))

        if not ctx.author.voice:
            await ctx.send("Connect to a voice channel!")
            return

        voice_channel = ctx.author.voice.channel
        noshuffle = False
        cmds = {"-"+genre for genre in pl_id.keys()}
        args = set(args)

        if "-ns" in args:
            noshuffle = True
            args.remove("-ns")

        try:
            genre = args.intersection(cmds).pop()
            args.remove(genre)
        except:
            genre = "-default"

        chart = get_chart(genre[1:])

        try:
            maxsongs = args.pop()
        except:
            maxsongs = None

        if maxsongs:
            if not maxsongs.isnumeric():
                print(
                    f"[{getHoursMinutes()}][service:error] Argument is not a number")
                await ctx.send(f"[{getHoursMinutes()}][service:error] Argument is not a number")
                return
            maxsongs = int(maxsongs)
        else:
            maxsongs = 15

        if len(chart) < maxsongs:
            maxsongs = len(chart)

        if not noshuffle:
            random.shuffle(chart)

        await ctx.send(str(maxsongs) + (" songs " if maxsongs > 1 else " song ") + "added to the queue!")
        songs = [None] * maxsongs

        # _songs = [["Pos.", "Title", "Artist"]]
        _songs = []

        print(f"Retrieving {maxsongs} songs of the '{genre}' genre...")
        query = chart[0]["Artist"] + " " + chart[0]["TrackName"] + " lyrics"
        await self.play(ctx, query + " -nv")
        _songs.append([1, chart[0]["TrackName"], chart[0]["Artist"]])

        threads = []
        for i in range(1,  maxsongs):
            query = chart[i]["Artist"] + " " + \
                chart[i]["TrackName"] + " lyrics"
            _songs.append([i+1, chart[i]["Artist"], chart[i]["TrackName"]])

            _t = threading.Thread(target=wrap_async_func, args=(query, i))
            threads.append(_t)

        for t in threads:
            await asyncio.sleep(0.1)
            t.start()

        for t_ in threads:
            t_.join()

        print(tabulate(_songs,)
              #    headers=["Pos.", "Title", "Artist"])
              )
        print("All songs downloaded.")

        for song in songs[1:]:
            self.music_queue.append(song)

        self.top_playing = True

    @commands.command(name="nowplaying", aliases=["np"], help="Returns the title of the song currently playing")
    async def nowplaying(self, ctx, *args):
        if self.vc != None:
            if self.now_playing:
                await ctx.send(self.now_playing + " is now playing")
            else:
                await ctx.send("No song playing")
        else:
            await ctx.send("Not connected to a voice channel")

    @commands.command(name="radio", help="Streams a web radio")
    async def radio(self, ctx,  url: str = 'http://stream.radioparadise.com/rock-128'):
        self.is_radio_playing = True
        await self.clear(ctx)
        channel = ctx.message.author.voice.channel
        try:
            self.vc = await channel.connect()
        except:
            pass
        self.vc.play(discord.FFmpegPCMAudio(
            # 'https://stream.streambase.ch/radio24/mp3-192'))
            # 'http://icy.unitedradio.it/SubasioPiu.mp3'))
            # 'http://onair11.xdevel.com:8050'))
            # 'http://shoutcast.rtl.it:3010/'))
            # 'http://192.111.140.6:9683/stream'))
            'http://0n-pop.radionetz.de/0n-pop.mp3'))
            # 'https://stream.0nlineradio.com/k-pop?ref'))
            # 'http://stream.radioparadise.com/rock-128'))

    @commands.command(name="loopqueue", aliases=["lq", "loopq"], help="Loops the queue")
    async def loopqueue(self, ctx):
        self.loop_queue = not self.loop_queue
        msg = "Now looping the queue" if self.loop_queue else "Queue looping removed"
        await ctx.send(msg)
        print(msg)

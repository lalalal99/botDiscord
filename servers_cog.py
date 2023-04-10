import asyncio
import os
import subprocess
import time
from datetime import datetime
from importlib.resources import path
from pprint import isreadable
from traceback import print_tb

import discord
import pytz
from discord.ext import commands, tasks


def capitalize(word):
    return word[0].upper() + word[1:]


def getHoursMinutes():
    return datetime.now(pytz.timezone("Europe/Rome")).strftime("%H:%M")


async def error_title_not_in_list(ctx, query, titles):
    msg = "Failed to recognize '" + query + "', try the followings:\n"
    for title in titles.keys():
        msg += (title + "\n")
    await ctx.send(msg)


def user_has_permission(ctx):
    permissionRole = "-"
    role = discord.utils.get(ctx.guild.roles, name=permissionRole)
    roles = ctx.author.roles
    return role in roles


def process_exists(title):
    process_name = "Server " + capitalize(title)
    call = 'TASKLIST', '/FI', 'windowtitle eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode("windows-1252")
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # last_line equals "criteri specificati." if the process does not exist
    return not last_line.startswith("criteri")


class servers_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = "D:\\FRANCESCO\\shortcutServers\\"
        self.titles = {}

    def getTitles(self):
        # removes "start_" and ".bat" from file name
        titles = [filename[6:-4] for filename in os.listdir(self.path)]
        return {title: {"timer": 0} for title in titles}

    @ tasks.loop(seconds=5)
    async def status_task(self):
        currently_running = list(filter(process_exists, self.titles))

        if currently_running:
            available_time = 5 / len(currently_running)
            for title in currently_running:
                await self.bot.change_presence(activity=discord.Game(capitalize(title)))
                await asyncio.sleep(available_time)
        else:
            await self.bot.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name='Shrek 2'))

    @ commands.Cog.listener()
    async def on_ready(self):
        self.titles = self.getTitles()
        self.status_task.start()

    @ commands.command(name="sstart", help="Starts a server")
    async def sstart(self, ctx, *args):
        if not user_has_permission(ctx):
            await ctx.send("You are not allowed to use this command")
            return

        query = " ".join(args).lower()

        if query not in self.titles.keys():
            await error_title_not_in_list(ctx, query, self.titles)
            return

        await self.runServer(query, ctx)

    async def runServer(self, title, ctx):
        if process_exists(title):
            error_msg = f"[server:error] {capitalize(title)} server is already running"
            print(f"[{getHoursMinutes()}]"+error_msg)
            await ctx.send(error_msg)
            return

        self.titles[title]["timer"] = time.time()

        nomeFile = "start_" + title + ".bat"
        path = os.path.join(self.path, nomeFile)

        SW_MINIMIZE = 6
        info = subprocess.STARTUPINFO()
        info.dwFlags = subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = SW_MINIMIZE
        subprocess.Popen(path, startupinfo=info,
                         creationflags=subprocess.CREATE_NEW_CONSOLE)

        print(
            f"[{getHoursMinutes()}][server:start] {capitalize(title)} server started")
        await ctx.send(f"[server:start] {capitalize(title)} server started")

    @ commands.command(name="sstop", help="Stops a server")
    async def sstop(self, ctx, *args):
        if not user_has_permission(ctx):
            await ctx.send("You are not allowed to use this command")
            return

        query = " ".join(args).lower()

        if query not in self.titles.keys():
            await error_title_not_in_list(ctx, query, self.titles)
            return

        await self.stopServer(query, ctx)

    async def stopServer(self, title, ctx):
        if not process_exists(title):
            error_msg = f"[server:error] {capitalize(title)} server is not running"
            print(f"[{getHoursMinutes()}]"+error_msg)
            await ctx.send(error_msg)
            return

        tmp = time.time()

        if tmp - self.titles[title]["timer"] < 70:
            time_remaining = 70 - int(tmp - self.titles[title]['timer'])
            minutes = int(time_remaining/60)
            seconds = time_remaining % 60
            time_remaining = f"{minutes}:{'0'+f'{seconds}' if seconds - 10 < 0 else seconds}" if time_remaining >= 60 else time_remaining
            await ctx.send(f"[server:notice] Please wait {time_remaining}s")
            return

        self.titles[title]["timer"] = 0

        cmd = 'taskkill /FI "WINDOWTITLE eq Server ' + capitalize(title) + '"'
        os.system(cmd)

        print(
            f"[{getHoursMinutes()}][server:stop] {capitalize(title)} server shut down")
        await ctx.send(f"[server:stop] {capitalize(title)} server shut down")

    @ commands.command(name="srestart", help="Restarts a server")
    async def srestart(self, ctx, *args):
        if not user_has_permission(ctx):
            await ctx.send("You are not allowed to use this command")
            return

        query = " ".join(args).lower()

        if query not in self.titles.keys():
            await error_title_not_in_list(ctx, query, self.titles)
            return

        if not process_exists(query):
            error_msg = f"[server:error] {capitalize(query)} server is not running"
            print(f"[{getHoursMinutes()}]"+error_msg)
            await ctx.send(error_msg)
            return

        await self.stopServer(query, ctx)
        while(process_exists(query)):
            time.sleep(1)
        await self.runServer(query, ctx)

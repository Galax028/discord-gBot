# pylint: disable=import-error, no-name-in-module

import asyncio
import os
import sqlite3
import sys

import aiosqlite
import discord
from discord.ext import commands
from gServerTools import criticallog, infolog, successlog

from lib.conf_importer import token, version


class gBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=self.get_prefix,
                         help_command=kwargs["help_cmd"],
                         case_insensitive=True,
                         status=kwargs["status"],
                         activity=kwargs["activity"])

        self.token = kwargs["token"]
        self.dbpath = kwargs["dbpath"]
        self.load_cogs = kwargs["load_cogs"]
        self.jishaku = kwargs["jishaku"]

    def run(self):
        if self.load_cogs == True:
            self.cogloader()
        
        if self.jishaku == True:
            infolog("SETUP: Loading Jishaku...")
            super().load_extension("jishaku")
            successlog("SETUP:     └╴Jishaku has been loaded.")

        asyncio.run(self.dbloader())
        infolog("SETUP: Connecting to Discord API...")
        super().run(self.token)
    
    def cogloader(self):
        infolog("SETUP: Loading cogs...")
        for file in os.listdir("Python/discord-gBot/cogs"):
            if file.endswith(".py"):
                try:
                    super().load_extension(f'cogs.{file[:-3]}')
                    successlog(f"SETUP:     └╴Cog {file} is now loaded.")
                except Exception as e:
                    criticallog(f"SETUP:     └╴A critical error occurred while loading cog {file}.")
                    criticallog(f"SETUP:         └╴{e.__class__.__name__}: {e}")

    async def dbloader(self):
        infolog("SETUP: Checking Sqlite database...")
        async with aiosqlite.connect(self.dbpath) as db:
            try:
                await db.execute("SELECT * FROM guild_config")
                successlog("SETUP:     └╴guild_config table found.")
                await db.execute("SELECT * FROM datastore")
                successlog("SETUP:     └╴datastore table found.")
            except sqlite3.OperationalError:
                criticallog("SETUP:     └╴Sqlite database corrupted. Aborting setup process.")
                sys.exit(1)
        successlog("SETUP:     └╴Sqlite database check completed.")
    
    async def on_ready(self):
        successlog("SETUP:     └╴Connected to Discord API.")
        infolog("gBot is now online.")
    
    async def get_prefix(self, message):
        guild_id = message.guild.id
        async with aiosqlite.connect(self.dbpath) as db:
            try:
                async with db.execute("""SELECT prefix FROM guild_config WHERE guild_id=?""", (guild_id,)) as cursor:
                    prefix = await cursor.fetchone()
                    return prefix[0]
            except TypeError:
                await db.execute("""INSERT INTO guild_config (guild_id, prefix) VALUES (?, ?)""", (guild_id, "/"))
                await db.commit()
                return "/"


if __name__ == "__main__":
    os.system("")
    bot = gBot(token=token,
               dbpath="Python/discord-gBot/data/bot.db",
               load_cogs=True,
               jishaku=True,
               help_cmd=None,
               status=discord.Status.online,
               activity=discord.Game(f'/gbothelp | v.{version}'))
    bot.run()

import asyncio
import os
import sqlite3
import sys
from pathlib import Path

import aiohttp
import aiosqlite
import discord
from discord.ext import commands
from gServerTools import criticallog, infolog, successlog, warnlog

from lib.conf_importer import token, version


class gBot(commands.Bot):
    """
    Custom gBot class subclassed from `commands.Bot`.

    Attributes
    ----------
    `token` : `string`
        The bot token.

    `dbpath` : `string`
        The path of the sqlite database file.

    `load_cogs` : `bool`
        Tell the bot weather to load cogs or not.

    `jishaku` : `bool`
        Tell the bot weather to initialize Jishaku or not.

    `help_cmd` : `commands.HelpCommand`
        Specify the default help command for the bot.

    `status` : `discord.Status`
        Specify the bot's status. You need to also specify an activity to do this.

    `activity` : `discord.Activity`
        Specify the bot's activity. You need to also specify a status to do this.
    """

    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=self.get_prefix,
            help_command=kwargs["help_cmd"],
            case_insensitive=True,
            intents=discord.Intents.all(),
            status=kwargs["status"],
            activity=kwargs["activity"]
        )

        self.token = kwargs["token"]
        self.dbpath = kwargs["dbpath"]
        self.load_cogs = kwargs["load_cogs"]
        self.jishaku = kwargs["jishaku"]
        self.path = Path(__file__).parent.absolute()

    def run(self):
        if self.load_cogs:
            self.cogloader()

        if self.jishaku:
            asyncio.run(infolog("SETUP: Loading Jishaku..."))
            os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
            os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
            os.environ["JISHAKU_HIDE"] = "True"
            super().load_extension("jishaku")
            asyncio.run(successlog("SETUP:     └╴Jishaku has been loaded."))

        asyncio.run(self.dbloader())

        asyncio.run(infolog("SETUP: Connecting to Discord API..."))
        super().run(self.token)

    def cogloader(self):
        asyncio.run(infolog("SETUP: Loading cogs..."))
        for file in os.listdir(f"{self.path}/cogs"):
            if file.endswith(".py"):
                try:
                    super().load_extension(f'cogs.{file[:-3]}')
                    asyncio.run(successlog(f"SETUP:     └╴Cog {file} is now loaded."))
                except Exception as e:
                    asyncio.run(criticallog(f"SETUP:     └╴A critical error occurred while loading cog {file}."))
                    asyncio.run(criticallog(f"SETUP:         └╴{e.__class__.__name__}: {e}"))

    async def dbloader(self):
        await infolog("SETUP: Checking Sqlite database...")
        async with aiosqlite.connect(self.dbpath) as db:
            try:
                await db.execute("SELECT * FROM guild_config")
                await successlog("SETUP:     └╴guild_config table found.")
                await db.execute("SELECT * FROM datastore")
                await successlog("SETUP:     └╴datastore table found.")
            except sqlite3.OperationalError:
                await criticallog("SETUP:     └╴Sqlite database corrupted. Aborting setup process.")
                sys.exit(1)
        await successlog("SETUP:     └╴Sqlite database check completed.")

    async def on_connect(self):
        await successlog("SETUP:     └╴Connected to Discord API. Readying up...")

    async def on_ready(self):
        await infolog("SETUP:        └╴Readied up.")
        await infolog("Starting AioHTTP client session...")
        self.cs = aiohttp.ClientSession()
        await successlog("    └╴AioHTTP client session started. Setup completed.")

    async def get_prefix(self, message):
        guild_id = message.guild.id
        async with aiosqlite.connect(self.dbpath) as db:
            try:
                async with db.execute("""SELECT prefix FROM guild_config WHERE guild_id=?""", (guild_id,)) as cursor:
                    prefix = await cursor.fetchone()
                    return prefix[0]
            except TypeError:
                await db.execute(
                    """INSERT INTO guild_config (guild_id, prefix, pagination, captcha_channel_id)
                       VALUES (?, ?, ?, ?)""", (guild_id, "/", "auto", 0)
                )
                await db.commit()
                return "/"


if __name__ == "__main__":
    bot = gBot(
        token=token,
        dbpath=f"{Path(__file__).parent.absolute()}/data/bot.db",
        load_cogs=True,
        jishaku=True,
        help_cmd=None,
        status=discord.Status.online,
        activity=discord.Game(f'/gbothelp | v.{version}')
    )
    bot.run()

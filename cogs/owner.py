# pylint: disable=import-error, no-name-in-module

import asyncio
import os
import random
from typing import Optional

import aiosqlite
import discord
import sqlite_formatter as sf
from discord.ext import commands
from discord.utils import get
from gServerTools import criticallog, infolog, successlog
from lib.conf_importer import token


class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="read-sql-table")
    async def read_sql_table(self, ctx, table: str):
        result = await sf.aio_read_table(
            table=table,
            conn=f"{self.bot.path}/data/bot.db"
        )
        await ctx.send(f"```\n{result}\n```")
    
    @commands.command(name="read-sql-query")
    async def read_sql_query(self, ctx, table: str, column: str, *, query: str):
        if not query.startswith("SELECT"):
            return await ctx.send("Query needs to be a SELECT statement.")
        
        result = await sf.aio_read_query(
            query=query,
            conn=f"{self.bot.path}/data/bot.db",
            table=table,
            column=column
        )
        await ctx.send(f"```\n{result}\n```")
    
    @commands.command()
    async def sql(self, ctx, *, query: str):
        if query.startswith("SELECT"):
            return await ctx.send("Please use `read-sql-query` for SELECT statements.")

        async with aiosqlite.connect(f"{self.bot.path}/data/bot.db") as db:
            await db.execute(query)
            await db.commit()
        await ctx.send("SQL operation completed.")

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(f"cogs.{cog if not cog.endswith('.py') else cog[:-3]}")
        except Exception as e:
            await ctx.send(f"An error occurred while trying to load the cog `{cog}`.")
            await ctx.send(f"{e.__class__.__name__}: {e}")
            await criticallog(f"Failed to load cog {cog}.")
            await criticallog(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"Loaded cog `{cog}` successfully.")
            await successlog(f"Cog {cog} is now loaded.")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(f"cogs.{cog[:-3]}")
        except Exception as e:
            await ctx.send(f"An error occurred while trying to unload the cog `{cog if not cog.endswith('.py') else cog[:-3]}`.")
            await ctx.send(f"{e.__class__.__name__}: {e}")
            await criticallog(f"Failed to unload cog {cog}.")
            await criticallog(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"Unloaded cog `{cog}` successfully.")
            await successlog(f"Cog {cog} is now unloaded.")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        if cog == "all" or cog == "*":
            for filename in os.listdir(f"{self.bot.path}/cogs"):
                if filename.endswith('.py'):
                    try:
                        self.bot.reload_extension(f"cogs.{filename[:-3]}")
                    except Exception as e:
                        await ctx.send(f"An error occurred while trying to reload the cog `{filename}`.")
                        await ctx.send(f"{e.__class__.__name__}: {e}")
                        await criticallog(f"Failed to reload cog {filename}.")
                        await criticallog(f"{e.__class__.__name__}: {e}")
                    else:
                        await successlog(f"Cog {filename} is now reloaded.")
                        await ctx.send(f"Reloaded cog `{filename}` successfully.")
        else:
            try:
                self.bot.reload_extension(f"cogs.{cog if not cog.endswith('.py') else cog[:-3]}")
            except Exception as e:
                await ctx.send(f"An error occurred while trying to unload the cog `{cog if not cog.endswith('.py') else cog[:-3]}`.")
                await ctx.send(f"{e.__class__.__name__}: {e}")
                await criticallog(f"Failed to unload cog {cog}.")
                await criticallog(f"{e.__class__.__name__}: {e}")
            else:
                await ctx.send(f"Reloaded cog `{cog}` successfully.")
                await successlog(f"Cog {cog} is now unloaded.")

    @commands.command()
    @commands.is_owner()
    async def pull(self, ctx):
        await ctx.send("Pulling from GitHub...")
        await asyncio.create_subprocess_shell("g gbot update")
        await ctx.send("Restarting...")
        await infolog("gBot has been shutted down.")
        await self.bot.logout()
        try: raise SystemExit(0)
        except: raise SystemExit(0)

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Are you sure you want to shutdown?(`y/n`,`10s timeout`):")
        msg = await self.bot.wait_for('message', timeout=10, check=lambda message: message.author == ctx.author)
        if msg.content.lower() == "y":
            await ctx.send("Logging Out...")
            await infolog("gBot has been shutted down.")
            await self.bot.logout()
            try: raise SystemExit(0)
            except: SystemExit(0)
        elif msg.content.lower() == "n":
            await ctx.send("Shutdown aborted.")
        elif msg.content.lower() != ["n","y"]:
            await ctx.send("Invalid response.")


def setup(bot):
    bot.add_cog(OwnerCog(bot))

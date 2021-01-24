import asyncio
import os
import random
import time
from contextlib import redirect_stdout
from io import StringIO

import discord
from discord.ext import commands
from lib.modules import token
from gServerTools import infolog, successlog, criticallog

async def password_randomizer():
    while True:
        global password
        genpass = [random.randint(0,9),random.randint(0,9),random.randint(0,9),random.randint(0,9),random.randint(0,9)]
        password = str(genpass).strip("[]'").replace(', ', '')
        successlog(f"[PRIORITY]ownercmd.py: The new password for /reqtoken is '{password}'.")
        await asyncio.sleep(3600)

class owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot_task = self.bot.loop.create_task(password_randomizer())

    @commands.command(name="evalulate")
    @commands.is_owner()
    async def _eval(self, ctx, parameter):
        stdout = StringIO()
        if parameter.startswith("```") and parameter.endswith("```"):
            with redirect_stdout(stdout):
                try:
                    parameter = parameter.replace("```", "")
                    exec(parameter)
                    await ctx.send(f"```{stdout.getvalue()}```")
                    stdout.close()
                except Exception as e:
                    await ctx.send(f"```{e.__class__.__name__}: {e}```")
        else:
            await ctx.send("Sorry, but you need to put the code you want to evalulate in a code block.")

    @commands.command()
    async def reqtoken(self, ctx):
        await ctx.send("Please type in the password. (`15s timeout`)")
        infolog(f"ownercmd.py: {ctx.message.author} has executed the command: reqtoken")
        msg = await self.bot.wait_for('message', timeout=15 ,check=lambda message: message.author == ctx.author)
        if msg.content.lower() == password:
            await ctx.send(f"Password is correct.\nThe token is: ||{token}||.")
        elif msg.content.lower() != password:
            await ctx.send("Password is incorrect.")

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(f"cogs.{cog[:-3]}")
        except Exception as e:
            await ctx.send(f"An error occurred while trying to load the cog `{cog}`.")
            await ctx.send(f"{e.__class__.__name__}: {e}")
            criticallog(f"[PRIORITY]ownercmd.py: Failed to load cog {cog}.")
            criticallog(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"Loaded cog `{cog}` successfully.")
            successlog(f"[PRIORITY]ownercmd.py: Cog {cog} is now loaded.")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(f"cogs.{cog[:-3]}")
        except Exception as e:
            await ctx.send(f"An error occurred while trying to unload the cog `{cog}`.")
            await ctx.send(f"{e.__class__.__name__}: {e}")
            criticallog(f"[PRIORITY]ownercmd.py: Failed to unload cog {cog}.")
            criticallog(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"Unloaded cog `{cog}` successfully.")
            successlog(f"[PRIORITY]ownercmd.py: Cog {cog} is now unloaded.")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(f"cogs.{cog[:-3]}")
            self.bot.load_extension(f"cogs.{cog[:-3]}")
        except Exception:
            await ctx.send(f"An error occurred while trying to reload the cog `{cog}`.")
            infolog(f"[PRIORITY]ownercmd.py: Failed to reload cog {cog}.")
        else:
            await ctx.send(f"Reloaded cog `{cog}` successfully.")
            successlog(f"[PRIORITY]ownercmd.py: Cog {cog} is now reloaded.")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Are you sure you want to shutdown?(`y/n`,`10s timeout`):")
        infolog(f"ownercmd.py: {ctx.message.author} has executed the command: shutdown")
        msg = await self.bot.wait_for('message', timeout=10 ,check=lambda message: message.author == ctx.author)
        if msg.content.lower() == "y":
            await ctx.send("Logging Out...")
            time.sleep(2)
            await ctx.send("It is now safe to kill the terminal.")
            infolog(f"[PRIORITY]ownercmd.py: gBot has been shutted down.")
            await self.bot.logout()
        elif msg.content.lower() == "n":
            await ctx.send("Shutdown aborted.")
        elif msg.content.lower() != ["n","y"]:
            await ctx.send("Invalid response.")

    @_eval.error
    async def _eval_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("This command can only be used by <@410424445216358410>.")

    @load.error
    async def load_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("This command can only be used by <@410424445216358410>.")

    @unload.error
    async def unload_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("This command can only be used by <@410424445216358410>.")

    @reload.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("This command can only be used by <@410424445216358410>.")

    @shutdown.error
    async def shutdown_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("This command can only be used by <@410424445216358410>.")

def setup(bot):
    bot.add_cog(owner(bot))

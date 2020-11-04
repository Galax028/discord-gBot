import asyncio
import os
import random
import time

import discord
from colorama import Fore, Style
from discord.ext import commands
from important.modules import token


async def password_randomizer():
    while True:
        global password
        genpass = [random.randint(0,9),random.randint(0,9),random.randint(0,9),random.randint(0,9),random.randint(0,9)]
        password = str(genpass).strip("[]'").replace(', ', '')
        print(f"{Fore.BLUE}[PRIORITY]ownercmd.py: The new password for /reqtoken is '{password}'.{Style.RESET_ALL}")
        await asyncio.sleep(1800)

class owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot_task = self.bot.loop.create_task(password_randomizer())

    @commands.command()
    async def reqtoken(self, ctx):
        await ctx.send("Please type in the password. (`15s timeout`)")
        print(f"Log/ownercmd.py: {ctx.message.author} has executed the command: reqtoken")
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
        except Exception:
            await ctx.send(f"An error occurred while trying to load the cog `{cog}`.")
            print(f"{Fore.RED}[PRIORITY]ownercmd.py: Failed to load cog {cog}.{Style.RESET_ALL}")
        else:
            await ctx.send(f"Loaded cog `{cog}` successfully.")
            print(f"{Fore.GREEN}[PRIORITY]ownercmd.py: Cog {cog} is now loaded.{Style.RESET_ALL}")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(f"cogs.{cog[:-3]}")
        except Exception:
            await ctx.send(f"An error occurred while trying to unload the cog `{cog}`.")
            print(f"{Fore.RED}[PRIORITY]ownercmd.py: Failed to unload cog {cog}.{Style.RESET_ALL}")
        else:
            await ctx.send(f"Unloaded cog `{cog}` successfully.")
            print(f"{Fore.GREEN}[PRIORITY]ownercmd.py: Cog {cog} is now unloaded.{Style.RESET_ALL}")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(f"cogs.{cog[:-3]}")
            self.bot.load_extension(f"cogs.{cog[:-3]}")
        except Exception:
            await ctx.send(f"An error occurred while trying to reload the cog `{cog}`.")
            print(f"{Fore.RED}[PRIORITY]ownercmd.py: Failed to reload cog {cog}.{Style.RESET_ALL}")
        else:
            await ctx.send(f"Reloaded cog `{cog}` successfully.")
            print(f"{Fore.GREEN}[PRIORITY]ownercmd.py: Cog {cog} is now reloaded.{Style.RESET_ALL}")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Are you sure you want to shutdown?(`y/n`,`10s timeout`):")
        print(f"Log/ownercmd.py: {ctx.message.author} has executed the command: shutdown")
        msg = await self.bot.wait_for('message', timeout=10 ,check=lambda message: message.author == ctx.author)
        if msg.content.lower() == "y":
            await ctx.send("Logging Out...")
            time.sleep(2)
            await ctx.send("It is now safe to kill the terminal.")
            print(f"{Fore.RED}[PRIORITY]ownercmd.py: gBot has been shutted down.{Style.RESET_ALL}")
            await self.bot.logout()
        elif msg.content.lower() == "n":
            await ctx.send("Shutdown aborted.")
        elif msg.content.lower() != ["n","y"]:
            await ctx.send("Invalid response.")

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

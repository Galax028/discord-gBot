# pylint: disable=import-error, no-name-in-module

import asyncio
import os
import random
import subprocess
import sys

import discord
from discord.ext import commands
from discord.utils import get
from gServerTools import criticallog, infolog, successlog
from lib.conf_importer import token


class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def panel(self, ctx):
        if ctx.invoked_subcommand is None:
            page1 = discord.Embed(title="gBot Remote Control Panel",
                                  description="`shutdown`",
                                  colour=discord.Colour.blurple())
            page1.add_field(name="This command will shutdown gBot.", value="React to ':ok:' to execute this.")
            page2 = discord.Embed(title="gBot Remote Control Panel",
                                  description="`reload`",
                                  colour=discord.Colour.blurple())
            page2.add_field(name="This command will reload all cogs.", value="React to ':ok:' to execute this.")
            page3 = discord.Embed(title="gBot Remote Control Panel",
                                  description="`reqtoken`",
                                  colour=discord.Colour.blurple())
            page3.add_field(name="This command will send the token.", value="React to ':ok:' to execute this.")

            contents = [page1, page2, page3]
            pages = 3
            cur_page = 1

            msg = await ctx.send(embed=(contents[cur_page - 1]))

            await msg.add_reaction("🆗")
            await msg.add_reaction("◀️")
            await msg.add_reaction("▶️")
            await msg.add_reaction("⏹️")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["🆗", "◀️", "▶️", "⏹️"]
                
            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)

                    if str(reaction.emoji) == "🆗":
                        if cur_page == 1:
                            await ctx.msg.delete()
                            await msg.delete()
                            await self.shutdown(ctx)
                            await msg.remove_reaction(reaction, user)
                        elif cur_page == 2:
                            await self.reload(ctx, cog="all")
                            await msg.remove_reaction(reaction, user)
                        else:
                            await self.reqtoken(ctx)
                            await msg.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        cur_page -= 1
                        await msg.edit(embed=(contents[cur_page - 1]))
                        await msg.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == "▶️" and cur_page != pages:
                        cur_page += 1
                        await msg.edit(embed=(contents[cur_page - 1]))
                        await msg.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == "⏹️":
                        await ctx.message.delete()
                        await msg.delete()
                        break

                    else:
                        await msg.remove_reaction(reaction, user)

                except asyncio.TimeoutError:
                    await ctx.msg.delete()
                    await msg.delete()
                    break

    @panel.command()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(f"cogs.{cog[:-3]}")
        except Exception as e:
            await ctx.send(f"An error occurred while trying to load the cog `{cog}`.")
            await ctx.send(f"{e.__class__.__name__}: {e}")
            await criticallog(f"Failed to load cog {cog}.")
            await criticallog(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"Loaded cog `{cog}` successfully.")
            await successlog(f"Cog {cog} is now loaded.")

    @panel.command()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(f"cogs.{cog[:-3]}")
        except Exception as e:
            await ctx.send(f"An error occurred while trying to unload the cog `{cog}`.")
            await ctx.send(f"{e.__class__.__name__}: {e}")
            await criticallog(f"Failed to unload cog {cog}.")
            await criticallog(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send(f"Unloaded cog `{cog}` successfully.")
            await successlog(f"Cog {cog} is now unloaded.")

    @panel.command()
    async def reload(self, ctx, *, cog: str):
        if cog == "all":
            for filename in os.listdir(f"{self.bot.path}/cogs"):
                if filename.endswith('.py'):
                    try:
                        self.bot.reload_extension(f"cogs.{filename[:-3]}")
                        await successlog(f"Cog {filename} is now reloaded.")
                        await ctx.send(f"Reloaded cog `{filename}` successfully.")
                    except Exception as e:
                        await ctx.send(f"An error occurred while trying to reload the cog `{filename}`.")
                        await ctx.send(f"{e.__class__.__name__}: {e}")
                        await criticallog(f"Failed to reload cog {filename}.")
                        await criticallog(f"{e.__class__.__name__}: {e}")

    @panel.command()
    async def updater(self, ctx):
        await ctx.send("Launching updater script...")
        if os.name == "nt":
            subprocess.Popen(["py", f"{self.bot.path}/update_wait.py"])
        else:
            subprocess.Popen(["bash", "#!bin/bash", f"python3 {self.bot.path}/updater.bash", "&"])
        await ctx.send("Logging Out...")
        await infolog(f"gBot has been shutted down.")
        await self.bot.logout()
        await self.bot.close()
        await asyncio.sleep(1)
        sys.exit(0)

    @panel.command()
    async def shutdown(self, ctx):
        await ctx.send("Are you sure you want to shutdown?(`y/n`,`10s timeout`):")
        msg = await self.bot.wait_for('message', timeout=10, check=lambda message: message.author == ctx.author)
        if msg.content.lower() == "y":
            await ctx.send("Logging Out...")
            await ctx.send("It is now safe to kill the terminal.")
            await infolog(f"gBot has been shutted down.")
            await self.bot.logout()
            await self.bot.close()
            await asyncio.sleep(1)
            sys.exit(0)
        elif msg.content.lower() == "n":
            await ctx.send("Shutdown aborted.")
        elif msg.content.lower() != ["n","y"]:
            await ctx.send("Invalid response.")


def setup(bot):
    bot.add_cog(OwnerCog(bot))

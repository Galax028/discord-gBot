# pylint: disable=import-error, no-name-in-module

import asyncio
import os
import random
import subprocess
import sys
from contextlib import redirect_stdout
from io import StringIO

import discord
from discord.ext import commands
from discord.utils import get
from gServerTools import criticallog, infolog, successlog
from lib.conf_importer import token


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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 410424445216358410:
            if message.content.lower() == "/panel":
                shutdown_cmd = get(self.bot.commands, name="shutdown")
                reload_cmd = get(self.bot.commands, name="reload")
                reqtoken_cmd = get(self.bot.commands, name="reqtoken")

                page1 = discord.Embed(title="gBot Remote Control Panel",
                                      description="`shutdown`",
                                      colour=discord.Colour.blurple())
                page1.add_field(name=f"{shutdown_cmd.help}", value="React to ':ok:' to execute this.")
                page2 = discord.Embed(title="gBot Remote Control Panel",
                                      description="`reload`",
                                      colour=discord.Colour.blurple())
                page2.add_field(name=f"{reload_cmd.help}", value="React to ':ok:' to execute this.")
                page3 = discord.Embed(title="gBot Remote Control Panel",
                                      description="`reqtoken`",
                                      colour=discord.Colour.blurple())
                page3.add_field(name=f"{reqtoken_cmd.help}", value="React to ':ok:' to execute this.")

                ctx = await self.bot.get_context(message)
                contents = [page1, page2, page3]
                pages = 3
                cur_page = 1

                msg = await message.channel.send(embed=(contents[cur_page - 1]))

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
        else:
            pass

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

    @commands.command(help="This command will send the bot token if the password is correct.")
    async def reqtoken(self, ctx):
        await ctx.send("Please type in the password. (`15s timeout`)")
        infolog(f"ownercmd.py: {ctx.message.author} has executed the command: reqtoken")
        try:
            msg = await self.bot.wait_for('message', timeout=15 ,check=lambda message: message.author == ctx.author)
            if msg.content.lower() == password:
                await ctx.send(f"Password is correct.\nThe token is: ||{token}||.")
            elif msg.content.lower() != password:
                await ctx.send("Password is incorrect.")
        except asyncio.TimeoutError:
            await ctx.send("Took too long.")

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

    @commands.command(help="This command will make gBot reload all cogs except ownercmd.py.")
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        if cog == "all":
            for filename in os.listdir('Python\\discord-gBot\\cogs'):
                if filename.startswith('ownercmd'):
                    pass
                elif filename.endswith('.py'):
                    try:
                        self.bot.unload_extension(f'cogs.{filename[:-3]}')
                        self.bot.load_extension(f'cogs.{filename[:-3]}')
                        successlog(f"[PRIORITY]botrun.py: Cog {filename} is now reloaded.")
                        await ctx.send(f"Reloaded cog `{filename}` successfully.")
                    except Exception as e:
                        await ctx.send(f"An error occurred while trying to reload the cog `{filename}`.")
                        await ctx.send(f"{e.__class__.__name__}: {e}")
                        criticallog(f"[PRIORITY]ownercmd.py: Failed to reload cog {filename}.")
                        criticallog(f"{e.__class__.__name__}: {e}")
        else:
            try:
                self.bot.unload_extension(f"cogs.{cog[:-3]}")
                self.bot.load_extension(f"cogs.{cog[:-3]}")
                await ctx.send(f"Reloaded cog `{cog}` successfully.")
                successlog(f"[PRIORITY]ownercmd.py: Cog {cog} is now reloaded.")
            except Exception as e:
                await ctx.send(f"An error occurred while trying to reload the cog `{cog}`.")
                await ctx.send(f"{e.__class__.__name__}: {e}")
                criticallog(f"[PRIORITY]ownercmd.py: Failed to reload cog {cog}.")
                criticallog(f"{e.__class__.__name__}: {e}")

    @commands.command(help="This command shuts gBot down and launch the update_wait.py script.")
    @commands.is_owner()
    async def updater(self, ctx):
        await ctx.send("Launching updater script...")
        if os.name == "nt":
            subprocess.Popen(["py", "Python\\discord-gBot\\update_wait.py"])
        else:
            subprocess.Popen(["bash", "python3", "Python\\discord-gBot\\update_wait.py", "&"])
        await ctx.send("Logging Out...")
        infolog(f"[PRIORITY]ownercmd.py: gBot has been shutted down.")
        await self.bot.logout()
        sys.exit(0)

    @commands.command(help="This command shuts gBot down.")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Are you sure you want to shutdown?(`y/n`,`10s timeout`):")
        infolog(f"ownercmd.py: {ctx.message.author} has executed the command: shutdown")
        msg = await self.bot.wait_for('message', timeout=10 ,check=lambda message: message.author == ctx.author)
        if msg.content.lower() == "y":
            await ctx.send("Logging Out...")
            await ctx.send("It is now safe to kill the terminal.")
            infolog(f"[PRIORITY]ownercmd.py: gBot has been shutted down.")
            await self.bot.logout()
            sys.exit(0)
        elif msg.content.lower() == "n":
            await ctx.send("Shutdown aborted.")
        elif msg.content.lower() != ["n","y"]:
            await ctx.send("Invalid response.")


def setup(bot):
    bot.add_cog(owner(bot))

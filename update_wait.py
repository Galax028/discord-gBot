import sys

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from gServerTools import errorlog, successlog

from lib.conf_importer import token, version


bot = commands.Bot(command_prefix="/", case_insensitive=True, help_command=None)

@bot.event
async def on_ready():
    successlog("[PRIORITY]update_wait.py: gBot updater is now online.")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(f'/gbothelp | v.{version}'))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        embed = discord.Embed(title="Sorry for the inconvenience!",
                              description="gBot is going through a maintaince period right now, please wait until gBot's status become online. Then you will be able to use gBot again.",
                              colour=discord.Colour.red())
        await ctx.send(embed=embed)
    else:
        errorlog(f"{error.__class__.__name__}: {error}")

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Are you sure you want to shutdown?(`y/n`,`10s timeout`):")
    msg = await bot.wait_for('message', timeout=10 ,check=lambda message: message.author == ctx.author)
    if msg.content.lower() == "y":
        await ctx.send("Logging Out...")
        await ctx.send("It is now safe to kill the terminal.")
        await bot.logout()
        sys.exit(0)
    elif msg.content.lower() == "n":
        await ctx.send("Shutdown aborted.")
    elif msg.content.lower() != ["n","y"]:
        await ctx.send("Invalid response.")

bot.run(token)

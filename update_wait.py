import sys
from pathlib import Path

import aiosqlite
import discord
from discord.ext import commands
from gServerTools import errorlog, successlog

from lib.conf_importer import token, version


async def get_prefix(self, message):
    guild_id = message.guild.id
    async with aiosqlite.connect(f"{Path(__file__).parent.absolute()}/data/bot.db") as db:
        try:
            async with db.execute("""SELECT prefix FROM guild_config WHERE guild_id=?""", (guild_id,)) as cursor:
                prefix = await cursor.fetchone()
                return prefix[0]
        except TypeError:
            await db.execute("""INSERT INTO guild_config (guild_id, prefix) VALUES (?, ?)""", (guild_id, "/"))
            await db.commit()
            return "/"


bot = commands.Bot(command_prefix=get_prefix,
                   case_insensitive=True,
                   help_command=None,
                   status=discord.Status.dnd,
                   activity=discord.Game("Currently on maintainance!"))


@bot.event
async def on_ready():
    successlog("gBot updater is now online.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Sorry for the inconvenience!",
                              description="gBot is going through a maintenance period right now, please wait until gBot's status become online. Then you will be able to use gBot again.",
                              colour=discord.Colour.red())
        await ctx.send(embed=embed)
    else:
        errorlog(f"{error.__class__.__name__}: {error}")


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Are you sure you want to shutdown?(`y/n`,`10s timeout`):")
    msg = await bot.wait_for('message', timeout=10, check=lambda message: message.author == ctx.author)
    if msg.content.lower() == "y":
        await ctx.send("Logging Out...")
        await ctx.send("It is now safe to kill the terminal.")
        await bot.logout()
        sys.exit(0)
    elif msg.content.lower() == "n":
        await ctx.send("Shutdown aborted.")
    elif msg.content.lower() != ["n", "y"]:
        await ctx.send("Invalid response.")

bot.run(token)

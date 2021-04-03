# pylint: disable=import-error, no-name-in-module

import aiosqlite
import discord
from discord.ext import commands
from gServerTools import errorlog, infolog, successlog

from lib.conf_importer import version


class MetaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dbpath = self.bot.dbpath

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.NotOwner):
            return await ctx.send("Sorry, but this command can only be used by the owner of gBot.")
        if isinstance(error, commands.MissingPermissions):
            errorEmbed = discord.Embed(
                title=":x: You do not have sufficient permissions!",
                description=f"See the error message below for more details.\n```py\n{error}\n```"
            )
            return await ctx.send(embed=errorEmbed)
        if isinstance(error, commands.MissingRequiredArgument):
            errorEmbed = discord.Embed(
                title=":x: You are missing required arguments!",
                description=f"See the error message below for more details.\n```py\n{error}\n```"
            )
            return await ctx.send(embed=errorEmbed)
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"Woah, slow down! This command is on cooldown. You need to wait {error.retry_after} more.")
        if isinstance(error, commands.NSFWChannelRequired):
            return await ctx.send("Sorry, but this command can only be used in NSFW channels.")
        if isinstance(error, commands.BotMissingPermissions):
            return
        if isinstance(error, commands.CommandInvokeError):
            errorEmbed = discord.Embed(
                title=":x: An Error Occurred!",
                description="If you believe that this is a bug, please report it in our [support server](https://discord.gg/2hVmdnb).",
                colour=discord.Colour.red()
            )
            errorEmbed.add_field(
                name="** **",
                value=f"```py\nAn exception occurred in the command {ctx.command}:\n    └╴{error.__class__.__name__}:\n        └╴{error.original}```"
            )
            await errorlog(f"An exception occurred in the command {ctx.command}:")
            await errorlog(f"    └╴{error.original.__class__.__name__}:")
            await errorlog(f"        └╴{error.original}")
            return await ctx.send(embed=errorEmbed)
        else:
            errorEmbed = discord.Embed(
                title=":x: An Error Occurred!",
                description="If you believe that this is a bug, please report it in our [support server](https://discord.gg/2hVmdnb).",
                colour=discord.Colour.red()
            )
            errorEmbed.add_field(
                name="** **",
                value=f"```py\nAn exception occurred in the command {ctx.command}:\n    └╴{error.__class__.__name__}:\n        └╴{error}```"
            )
            await errorlog(f"An exception occurred in the command {ctx.command}:")
            await errorlog(f"    └╴{error.__class__.__name__}:")
            await errorlog(f"        └╴{error}")
            return await ctx.send(embed=errorEmbed)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        await infolog(f"{ctx.message.author} has executed the command: {ctx.command}.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        async with aiosqlite.connect(self.dbpath) as db:
            await db.execute("""INSERT INTO guild_config (guild_id, prefix, pagination) VALUES (?, ?, ?)""", (guild.id, "/", "auto"))
            await db.commit()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        async with aiosqlite.connect(self.dbpath) as db:
            await db.execute("""DELETE FROM guild_config WHERE guild_id=?""", (guild.id,))
            await db.commit()


def setup(bot):
    bot.add_cog(MetaCog(bot))

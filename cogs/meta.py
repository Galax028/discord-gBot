# pylint: disable=import-error, no-name-in-module

import aiosqlite
import discord
from discord.ext import commands
from gServerTools import errorlog, successlog

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
            return await ctx.send("Sorry, but you don't have permissions to do that.")
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(error)
        if isinstance(error, commands.BotMissingPermissions):
            return
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
            errorEmbed = discord.Embed(title=":x: An Error Occurred!",
                                       description="If you believe that this is a bug, please report it in our [support server](https://discord.gg/2hVmdnb).",
                                       colour=discord.Colour.red())
            errorEmbed.add_field(name="** **",
                                 value=f"```py\nAn exception occurred in the command {ctx.command}:\n    └╴{error.__class__.__name__}:\n        └╴{error}```")
            errorlog(f"An exception occurred in the command {ctx.command}:")
            errorlog(f"    └╴{error.__class__.__name__}:")
            errorlog(f"        └╴{error}")
            return await ctx.send(embed=errorEmbed)
        else:
            errorEmbed = discord.Embed(title=":x: An Error Occurred!",
                                       description="If you believe that this is a bug, please report it in our [support server](https://discord.gg/2hVmdnb).",
                                       colour=discord.Colour.red())
            errorEmbed.add_field(name="** **",
                                 value=f"```py\nAn exception occurred in the command {ctx.command}:\n    └╴{error.__class__.__name__}:\n        └╴{error}```")
            errorlog(f"An exception occurred in the command {ctx.command}:")
            errorlog(f"    └╴{error.__class__.__name__}:")
            errorlog(f"        └╴{error}")
            return await ctx.send(embed=errorEmbed)

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

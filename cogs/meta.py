# pylint: disable=import-error, no-name-in-module

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from gServerTools import errorlog, successlog

from lib.conf_importer import version


class meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        successlog(f"[PRIORITY]meta.py: gBot is now online.")
        successlog(f"[PRIORITY]meta.py: The latency is {int(self.bot.latency * 1000)} ms.")
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'/gbothelp | v.{version}'))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        if isinstance(error, commands.NotOwner):
            await ctx.send("This command can only be used by <@410424445216358410>.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, but you don't have permissions to do that.")
        if isinstance(error, commands.MissingRequiredArgument):
            pass
        else:
            errorlog(f"metacmd.py: An exception occoured in the command {ctx.command}:")
            errorlog(f"metacmd.py:    {error.__class__.__name__}: {error}")
            await ctx.send(f"Sorry, but an error occurred while executing the command {ctx.command}!")
            await ctx.send(f"`{error.__class__.__name__}: {error}`")

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message) and message.mention_everyone is False:
            if 'fuck you' in message.content.lower():
                await message.channel.send('fuck you then')
            elif 'shit bot' in message.content.lower():
                await message.channel.send('then why tf you use me bro?????')
            elif 'help' in message.content.lower():
                await message.channel.send('What do you need help with?\n - use `/gbothelp` to see the full help\n - use `/gbotinfo` to see the info of gBot')
            elif 'im too lazy to program' in message.content.lower():
                await message.channel.send('then why did you create me in the first place bruh')
            else:
                pass


def setup(bot):
    bot.add_cog(meta(bot))

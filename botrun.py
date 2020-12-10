# pylint: disable-all
#DO NOT FORGET TO CHANGE TOKEN BEFORE UPLOADING

import json
import os

import discord
from colorama import Fore, Style
from discord.ext import commands
from discord.ext.commands import CommandNotFound

from important.modules import jsversion, prebuild, pyversion, token, version

#Bot Preparations
bot = commands.Bot(command_prefix = '/')
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f"{Fore.GREEN}[PRIORITY]botrun.py: gBot is now online.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[PRIORITY]botrun.py: The latency is {int(bot.latency * 1000)} ms.{Style.RESET_ALL}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f'/gbothelp | v.{version}'))

for filename in os.listdir('discord-gBot/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"{Fore.GREEN}[PRIORITY]botrun.py: Cog {filename} is now loaded.{Style.RESET_ALL}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return

#Bot Initialize
bot.run(token)
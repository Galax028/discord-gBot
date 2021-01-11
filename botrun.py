# pylint: disable-all
#DO NOT FORGET TO CHANGE TOKEN BEFORE UPLOADING

import json
import os

import discord
import gspread
from colorama import Fore, Style
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from oauth2client.service_account import ServiceAccountCredentials

from important.modules import jsversion, prebuild, pyversion, token, version

#Bot Preparations
bot = commands.Bot(command_prefix = '/')
bot.remove_command('help')

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("Python/creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("DB Test").sheet1

def get_table():
    return sheet.get_all_records()

@bot.event
async def on_ready():
    print(f"{Fore.GREEN}[PRIORITY]botrun.py: gBot is now online.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[PRIORITY]botrun.py: The latency is {int(bot.latency * 1000)} ms.{Style.RESET_ALL}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f'/gbothelp | v.{version}'))

for filename in os.listdir('Python/discord-gBot/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"{Fore.GREEN}[PRIORITY]botrun.py: Cog {filename} is now loaded.{Style.RESET_ALL}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message) and message.mention_everyone is False:
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
    await bot.process_commands(message)

@bot.command()
async def requestdb(ctx):
    await ctx.send(get_table())

@bot.command()
async def leaveserver(ctx):
    await ctx.send("Packing stuff up, I'm leaving VRV Yoshi server too L M A O")
    to_leave = bot.get_guild(749452197267243071)
    await to_leave.leave()

#Bot Initialize
bot.run(token)

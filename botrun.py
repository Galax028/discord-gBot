# pylint: disable-all
#DO NOT FORGET TO CHANGE TOKEN BEFORE UPLOADING

import json
import os

import discord
import gspread
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from gServerTools import criticallog, infolog, successlog
from oauth2client.service_account import ServiceAccountCredentials

from lib.modules import prebuild, token, version

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
    successlog(f"[PRIORITY]botrun.py: gBot is now online.")
    successlog(f"[PRIORITY]botrun.py: The latency is {int(bot.latency * 1000)} ms.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f'/gbothelp | v.{version}'))

for filename in os.listdir('Python\discord-gBot\cogs'):
    if filename.endswith('.py'):
        cogs_list = []
        if filename.startswith('m_'):
            pass
        else:
            cogs_list.append(filename[:-3])
        
        for i in range(len(cogs_list)):
            try:
                bot.load_extension(f'cogs.{cogs_list[i]}')
                successlog(f"[PRIORITY]botrun.py: Cog {filename} is now loaded.")
            except Exception as e:
                criticallog(f"[PRIORITY]botrun.py: A critical error occurred while loading cog {filename}.")
                criticallog(f"{e.__class__.__name__}: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    else:
        raise error

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

#Bot Initialize
bot.run(token)

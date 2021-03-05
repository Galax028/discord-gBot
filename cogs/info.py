# pylint: disable=import-error, no-name-in-module

import asyncio
import os
import sys
from datetime import datetime, timedelta
from platform import python_version
from time import time
from typing import Optional

import aiosqlite
import discord
from discord import __version__ as discord_version
from discord.ext import commands
from discord.utils import get
from psutil import Process, virtual_memory

from cogs.anime import AnimeCog
from cogs.config import ConfigCog
from cogs.fun import FunCog
from cogs.mod import ModCog
import lib.utils as utils
from lib.conf_importer import prebuild, token, version
from lib.paginator import Paginator


def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(
                value) else f"<{key}>")

    params = " ".join(params)

    return f"`{cmd_and_aliases} {params}`"


def help_embed(page, cog_name):
    fields = []
    for cmd in cog_name.walk_commands(cog_name):
        fields.append((f"`{cmd}`", cmd.help, True))

    for name, value, inline in fields:
        page.add_field(name=name, value=value, inline=inline)

    return page


async def verification_channel_check(self, ctx):
    async with aiosqlite.connect(self.dbpath) as db:
        async with db.execute("""SELECT captcha_channel_id FROM guild_config WHERE guild_id=?""", (ctx.guild.id,)) as cursor:
            captcha_channel = await cursor.fetchone()
            try:
                if ctx.channel.id == int(captcha_channel[0]):
                    if str(ctx.command) != "verify":
                        await ctx.message.delete()
                        await ctx.send("You need to verify yourself to use this command.", delete_after=1)
                        raise commands.CommandNotFound()
            except TypeError:
                pass


class InfoCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.dbpath = self.bot.dbpath

    @commands.command(help="Displays information about gBot.")
    @commands.before_invoke(verification_channel_check)
    async def gbotinfo(self, ctx):
        embed = discord.Embed(title='About gBot',
                              colour=discord.Colour.blurple())

        proc = Process()
        with proc.oneshot():
            uptime = timedelta(seconds=time()-proc.create_time())
            cpu_time = timedelta(
                seconds=(cpu := proc.cpu_times()).system + cpu.user)
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        fields = [("Developed by:", "Galax028#9474", True),
                  ("Hosted using:", "https://mydiscordbothosting.com", True),
                  ("Version:", f"`{version}`", True),
                  ("Total Commands:", f"{len(self.bot.commands)}", True),
                  ("Invite the bot:",
                   "[Click Here](https://rb.gy/wzzuvm)", True),
                  ("Support Server:",
                   "[Click Here](https://discord.gg/2hVmdnb)", True),
                  ("⠀", "----------------------------------------------------------------------", False),
                  ("Python Version:", f"`{python_version()}`", True),
                  ("discord.py Version:", f"`{discord_version}`", True),
                  ("⠀", "⠀", True),
                  ("Uptime:", f"`{uptime}`", True),
                  ("CPU Time:", f"`{cpu_time}`", True),
                  ("RAM Usage:", f"`{mem_usage:,.3f}/150 MiB`", True),
                  ("⠀", "----------------------------------------------------------------------", False),
                  ("Special Thanks:",
                   "PixelEdition#2116, Marxist Gamer#3000, Sir.Nick#4646", False),
                  ("⠀", "⠀", False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Thank you for using gBot!")
        await ctx.send(embed=embed)

    @commands.command(help="Displays the gbot help page or displays help of a specific command.")
    @commands.before_invoke(verification_channel_check)
    @commands.bot_has_permissions(manage_messages=True)
    async def gbothelp(self, ctx, *, cmd: Optional[str]):
        if cmd is None:
            async with aiosqlite.connect(self.dbpath) as db:
                async with db.execute("""SELECT pagination FROM guild_config WHERE guild_id=?""", (ctx.guild.id,)) as cursor:
                    mode = await cursor.fetchone()
                    if mode[0] == "manual":
                        raise commands.BotMissingPermissions("Guild's pagination mode is manual.")

            contents = discord.Embed(title='gbothelp - Contents',
                                     description='Info Commands - Page 1\nFun Commands - Page 2\nAnime Commands - Page 3\nModeration Commands - Page 4\nConfiguration Commands - Page 5',
                                     colour=discord.Colour.blurple())
            page1 = discord.Embed(title='gbothelp - Info Commands',
                                  colour=discord.Colour.blurple())
            page2 = discord.Embed(title='gbothelp - Fun Commands',
                                  colour=discord.Colour.blurple())
            page3 = discord.Embed(title='gbothelp - Anime Commands',
                                  colour=discord.Colour.blurple())
            page4 = discord.Embed(title='gbothelp - Moderation Commands',
                                  colour=discord.Colour.blurple())
            page5 = discord.Embed(title='gbothelp - Configuration Commands',
                                  colour=discord.Colour.blurple())

            p = Paginator(bot=self.bot,
                          contents=[contents, help_embed(page1, InfoCog), help_embed(
                              page2, FunCog), help_embed(page3, AnimeCog), help_embed(page4, ModCog), help_embed(page5, ConfigCog)],
                          pages=5,
                          ctx=ctx,
                          user_id=ctx.author.id)
            await p.start_full()
        else:
            if (command := get(self.bot.commands, name=cmd)):
                embed = discord.Embed(title=f"gbothelp - `{command}`",
                                      description=' ',
                                      colour=discord.Colour.blurple())
                embed.add_field(name="Command Usage:",
                                value=syntax(command), inline=False)
                embed.add_field(name="Command Description:",
                                value=command.help, inline=False)
                await ctx.send(embed=embed)

            else:
                await ctx.send("Sorry, but that command does not exist.")

    @commands.command(help="Displays the ping of gBot.")
    @commands.before_invoke(verification_channel_check)
    async def ping(self, ctx):
        async def db_pinger(ctx):
            async with aiosqlite.connect(self.dbpath) as db:
                async with db.execute("""SELECT * FROM guild_config WHERE guild_id=?""", (ctx.guild.id,)) as cursor:
                    await cursor.fetchall()
        db_ping = await utils.timer(db_pinger(ctx))

        typing_ping = await utils.timer(ctx.send(":ping_pong: Pinging...", delete_after=0.1))

        embed = discord.Embed(title=":ping_pong: Pong!")
        embed.add_field(name=":electric_plug: Websocket Latency:",
                        value=f"`{(self.bot.latency * 1000):.2f} ms`", inline=False)
        embed.add_field(name=":keyboard: Typing Latency:",
                        value=f"`{typing_ping:.2f} ms`", inline=False)
        embed.add_field(name="<:database:815449617947688972> Database Latency:",
                        value=f"`{db_ping:.2f} ms`", inline=False)
        await ctx.send(embed=embed)

    @gbothelp.error
    async def gbothelp_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            contents = discord.Embed(title='gbothelp - Contents',
                                     description='Info Commands - Page 1\nFun Commands - Page 2\nAnime Commands - Page 3\nModeration Commands - Page 4\nConfiguration Commands - Page 5',
                                     colour=discord.Colour.blurple())
            page1 = discord.Embed(title='gbothelp - Info Commands',
                                  colour=discord.Colour.blurple())
            page2 = discord.Embed(title='gbothelp - Fun Commands',
                                  colour=discord.Colour.blurple())
            page3 = discord.Embed(title='gbothelp - Anime Commands',
                                  colour=discord.Colour.blurple())
            page4 = discord.Embed(title='gbothelp - Moderation Commands',
                                  colour=discord.Colour.blurple())
            page5 = discord.Embed(title='gbothelp - Configuration Commands',
                                  colour=discord.Colour.blurple())

            p = Paginator(bot=self.bot,
                          contents=[contents, help_embed(page1, InfoCog), help_embed(
                              page2, FunCog), help_embed(page3, AnimeCog), help_embed(page4, ModCog), help_embed(page5, ConfigCog)],
                          pages=5,
                          ctx=ctx,
                          user_id=ctx.author.id)
            await p.start_full_manual()


def setup(bot):
    bot.add_cog(InfoCog(bot))

import asyncio
import os
import sys
from datetime import datetime, timedelta
from platform import python_version
from time import time

import discord
from discord import __version__ as discord_version
from discord.ext import commands
from important.modules import jsversion, prebuild, pyversion, token, version
from psutil import Process, virtual_memory


def write_todo(write):
    with open('./important/todo.txt', 'w') as f:
        lines = f.writelines(write)
        return lines

def read_todo():
    with open('./important/todo.txt', 'r') as f:
        lines = f.readlines()
        return ' '.join(lines)

class info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gbotinfo(self, ctx):
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
                  ("Version:", f"Main: {version}\nPY: {pyversion}\nJS: {jsversion}", True),
                  ("Total Commands:", "31", True),
                  ("Invite the bot:", "[Click Here](https://rb.gy/wzzuvm)", True),
                  ("Support Server:", "[Click Here](https://discord.gg/2hVmdnb)", True),
                  ("⠀","----------------------------------------------------------------------", False),
                  ("Python Version:", f"`{python_version()}`", True),
                  ("discord.py Version:", f"`{discord_version}`", True),
                  ("⠀", "⠀", True),
                  ("Uptime:", f"`{uptime}`", True),
                  ("CPU Time:", f"`{cpu_time}`", True),
                  ("RAM Usage:", f"`{mem_usage:,.3f}/256 MiB`", True),
                  ("⠀","----------------------------------------------------------------------", False),
                  ("Special Thanks:", "PixelEdition#2116, Rage Gamer#3000, Nickfowa#4646", False),
                  ("⠀", "⠀", False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Thank you for using gBot!")
        await ctx.send(embed=embed)
        print(f"Log/botrun.py: {ctx.message.author} has executed the command: gbotinfo")

    @commands.command()
    async def updatelog(self, ctx):
        page1 = discord.Embed(title='gBot Update Log - Contents',
                              description='Beta 1 to 4 - Page 1\nVersion 1.0.0 to 1.x.x - Page 2',
                              colour=discord.Colour.blurple())
        page2 = discord.Embed(title='gBot Update Log - Beta 1 to 4',
                              description="Beta 1:\n- gBot is created\n- gbotinfo command\n\nBeta 2:\n- ping command\n- gbothelp command\n- 8ball command\n\nBeta 3:\n- clear command\n- gbotinfo command\n- tosscoin command\n- Clear command now clears the author's command\n- kick command\n- ban command\n- unban command\n- More fun commands added\n- Minor bug fixes\n\nBeta 4:\n- mute command\n- unmute command\n- Responses are now made into embeds\n\n`Page 1 out of 3`",
                              colour=discord.Colour.blurple())
        page3 = discord.Embed(title='gBot update Log - 1.0.0 to 1.3.0',
                              description="Version 1.0.0 - 1.0.3:\n- updatelog command\n- gbothelp command renovated\n- kickass command\n- space command\n- Bug fixes\n- mute command rewamp\n- kill command\n\nVersion 1.1.0 - 1.1.3:\n- gBot now uses cogs\n- UI improvements\n- wtodo command added\n- rtodo command added\n\nVersion 1.2.0 - 1.2.4:\n- gbotinfo command rewamp\n- New GitHub repository\n- Version detection\n- clear command additions\n- Code cleanup\n\nVersion 1.3.0:\n- load command\n- unload command\n- reload command\n- shutdown command\n- reqtoken command\n\n`Page 2 out of 3`",
                              colour=discord.Colour.blurple())
        page4 = discord.Embed(title='gBot Update Log - 2.0.0 to 2.x.x',
                              description="Version 2.0.0 - 2.0.3:\n- Music system\n- join command\n- play command\n- pause command\n- resume command\n- skip commmand\n- clearqueue command\n- stop command\n- disconnect command\n- Code cleanup\n\n`Page 3 out of 3`")

        contents = [page1, page2, page3, page4]
        pages = 4
        cur_page = 1
        message = await ctx.send(embed=(contents[cur_page-1]))
        print(f"Log/infocmd.py: {ctx.message.author} has executed the command: updatelog")

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=(contents[cur_page-1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=(contents[cur_page-1]))
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break

    @commands.command()
    async def gbothelp(self, ctx):
        page1 = discord.Embed(title='gBot Help - Contents',
                              description='Info Commands - Page 1\nFun Commands - Page 2\nModeration Commands - Page 3\nMusic Commands - Page 4\nSpecial Commands - Page 5',
                              colour=discord.Colour.blurple())
        page2 = discord.Embed(title='Info Commands',
                              description="gbotinfo - Displays information of gBot.\nupdatelog - Displays all of gBot's update log.\ngbothelp - Displays the gbot help page.\nupdatelog - Displays all of gBot's update logs.\nping - Displays the ping of gBot.\nwtodo <text>- Edit gBot's todo list. (owner only)\nrtodo - View gBot's todo list.\n\n`Page 1 out of 5`",
                              colour=discord.Colour.blurple())
        page3 = discord.Embed(title='Fun Commands',
                              description="8ball <question>- Ask the 8 ball and it will answer you.\ntosscoin <guess> - Guess if it's head or tails.\nspace - gBot will send a random picture of space.\nkickass <user> - Ass kickin' time!\nsad - Very sad.\nkill <user> - gBot will **try** to kill the user.\n\n`Page 2 out of 5`",
                              colour=discord.Colour.blurple())
        page4 = discord.Embed(title='Moderation Commands',
                              description='clear <amount> - gBot will clear messages.\nmute <user> <reason> - gBot will mute a user.\nunmute <user> - gBot will unmute a user.\nkick <user> <reason> - gBot will kick a user.\nban <user> <reason> - gBot will ban a user.\nunban <banned user> - gBot will unban a user.\n\n`Page 3 out of 5`',
                              colour=discord.Colour.blurple())
        page5 = discord.Embed(title='Music Commands',
                              description="join - gBot will join the voice channel that you're in.\nplay <YouTube URL> - gBot will play a song from youtube.\npause - gBot will pause the song.\nresume - gBot will resume the song.\nskip - gBot will skip the song.\nstop - gBot will stop playing songs.\nclearqueue - gBot will claer the music queue.\ndisconnect - gBot will disconnect from the voice channel\n\n`Page 4 out of 5`",
                              colour=discord.Colour.blurple())

        contents = [page1, page2, page3, page4, page5]
        pages = 5
        cur_page = 1
        message = await ctx.send(embed=(contents[cur_page-1]))
        print(f"Log/infocmd.py: {ctx.message.author} has executed the command: gbothelp")
        #sends the message

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            #this makes sure nobody except the author can interact with the menu

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                #waiting for a reaction to be added, times out after 60 seconds

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=(contents[cur_page-1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=(contents[cur_page-1]))
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    #removes reactions if the user tries to go forward on the last page or backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                #ending the loop if user doesn't react after 60 seconds

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title='Pong! :ping_pong:', description=f'The ping of gBot is `{int(self.bot.latency * 1000)}` ms!', colour=discord.Colour.blue())
        await ctx.send(embed=embed)
        print(f"Log/infocmd.py: {ctx.message.author} has executed the command: ping")

    @commands.command()
    async def wtodo(self, ctx, *, todo):
        if ctx.message.author.id == 410424445216358410:
            write_todo(write=todo)
            await ctx.send("gBot's todo list is now updated. Use `/rtodo` to see the todo list.")
            print(f"Log/infocmd.py: {ctx.message.author} has executed the command: wtodo")
        elif ctx.message.author.id != 410424445216358410:
            await ctx.send("Only gBot's developer can use this command. You can still use `/rtodo`.")

    @commands.command()
    async def rtodo(self, ctx):
        await ctx.send(f"**gBot's Todo List:**\n{read_todo()}")
        print(f"Log/infocmd.py: {ctx.message.author} has executed the command: rtodo")

    @wtodo.error
    async def wtodo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me what do you want to write on the todo list.')

def setup(bot):
    bot.add_cog(info(bot))

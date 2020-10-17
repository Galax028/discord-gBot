import os
import sys
import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import time

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
                              description="Version 2.0.0 - 2.x.x:\n- Leveling system\n- level command\n- readjson command\n\n`Page 3 out of 3`")

        contents = [page1, page2, page3,page4]
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
                              description='Info Commands - Page 1\nFun Commands - Page 2\nModeration Commands - Page 3\nLevel Commands - Page 4\nSpecial Commands - Page 5',
                              colour=discord.Colour.blurple())
        page2 = discord.Embed(title='Info Commands',
                              description="gbotinfo - Displays information of gBot.\nupdatelog - Displays all of gBot's update log.\ngbothelp - Displays the gbot help page.\nupdatelog - Displays all of gBot's update logs.\nping - Displays the ping of gBot.\nwtodo <text>- Edit gBot's todo list. (owner only)\nrtodo - View gBot's todo list.\n\n`Page 1 out of 4`",
                              colour=discord.Colour.blurple())
        page3 = discord.Embed(title='Fun Commands',
                              description="8ball <question>- Ask the 8 ball and it will answer you.\ntosscoin <guess> - Guess if it's head or tails.\nspace - gBot will send a random picture of space.\nkickass <user> - Ass kickin' time!\nsad - Very sad.\nkill <user> - gBot will **try** to kill the user.\n\n`Page 2 out of 4`",
                              colour=discord.Colour.blurple())
        page4 = discord.Embed(title='Moderation Commands',
                              description='clear <amount> - gBot will clear messages.\nmute <user> <reason> - gBot will mute a user.\nunmute <user> - gBot will unmute a user.\nkick <user> <reason> - gBot will kick a user.\nban <user> <reason> - gBot will ban a user.\nunban <banned user> - gBot will unban a user.\n\n`Page 3 out of 4`',
                              colour=discord.Colour.blurple())
        page5 = discord.Embed(title='Level Commands',
                              description='level - See what your level is.\nreadjson - Sends the json file for level storage.\n\n`Page 4 out of 5`',
                              colour=discord.Colour.blurple())
        page6 = discord.Embed(title='Special Commands',
                              description="reqtoken - Request gBot's token.\nload <cog> - Load a cog.\nunload <cog> - Unload a cog.\nreload <cog> - Reload a cog.\nshutdown - Shutdown gBot.\n\n`Page 5 out of 5`",
                              colour=discord.Colour.blurple())

        contents = [page1,page2,page3,page4,page5,page6]
        pages = 6
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
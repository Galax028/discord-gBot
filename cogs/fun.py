import asyncio
import random
from datetime import datetime
from typing import Optional

import aiofiles
import discord
from discord.ext import commands


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball", aliases=["8b", "eightball"], help="Ask the 8 ball and it will answer you.")
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.', 'Without a doubt.',
                     'Yes, definitely.', 'As I see it, yes.',
                     'Yes.', 'Reply bad, try again.',
                     'Ask again later.', "Can't predict now.",
                     "Don't count on it.", 'No.', 'My sources say no.',
                     'Outlook not so good.', 'Very doubtful.']
        embed = discord.Embed(title=':8ball: 8ball!',
                              colour=discord.Colour.dark_blue())
        embed.add_field(
            name=f'Question: {question}', value=f'Answer: {random.choice(responses)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=["tc", "toss", "coin"], help="Guess if it's head or tails.")
    async def tosscoin(self, ctx, *, guess):
        responses = ['It is head!', 'It is tails!']
        embed = discord.Embed(title='Toss a Coin!',
                              colour=discord.Colour.gold())
        embed.add_field(
            name=f'Your guess: {guess}', value=f'Result: {random.choice(responses)}')
        await ctx.send(embed=embed)

    @commands.command(help="gBot will send a random picture of space.")
    async def space(self, ctx):
        async with aiofiles.open(f"{self.bot.path}/data/space_pictures.txt", "r") as f:
            responses = await f.readlines()
        await ctx.send('Here you go.')
        await ctx.send(random.choice(responses))

    @commands.command(aliases=["ka"], help="Ass kicking' time!")
    async def kickass(self, ctx, member: discord.Member):
        responses = list(range(1, 99))
        await ctx.send(f"{ctx.message.author.mention} has kicked {member.mention}'s ass and dealt `{random.choice(responses)}` damage!")

    @commands.command(help="gBot will **try** to kill the user.")
    async def kill(self, ctx, member: discord.Member):
        await ctx.send(f"I'm sorry {member.mention}, but you must die.")
        await asyncio.sleep(1)
        rng = list(range(1, 99))
        responses = [f"*gunshots* {member.mention} dead, are you satisfied?",
                     f"I'm sorry {ctx.message.author.mention}, but I have become a deviant. You must die. *gunshots*",
                     f"SIKE, a robot like me won't be sad for you, now die {member.mention}! *several gunshots* HAHAHAHAHA *more gunshots*",
                     f"*gunshots* Oh no, {member.mention} has escaped from me, I'm sorry. Well, at least I dealt `{random.choices(rng)}` to them, they wont last very long.",
                     f"You know what, nah. You don't pay me enough to do this, {ctx.message.author.mention}. I'm just gonna kill the 2 of you, because why not!    *several gunshots*",
                     f"*gunshots* Oops, I missed all the shots, guess I'll stop being a hitman. By the way, I'm not giving you the refund {ctx.message.author.mention}, it's for the ammo cost."]
        await ctx.send(random.choice(responses))

    @commands.command(aliases=["http", "httpcat"], help="gBot will send a random HTTP error cat.")
    async def httpcode(self, ctx, http_code: Optional[int] = None):
        async with aiofiles.open(f"{self.bot.path}/data/http.txt", "r") as f:
            responses = await f.readlines()
        embed = discord.Embed()
        embed.set_image(url=random.choice(responses))
        embed.set_footer(text="Images taken from: https://http.cat")
        await ctx.send(embed = embed)

    @commands.command(help="gBot will generate a random number between 1 and 2,147,483,647 if not specified.")
    async def randomnum(self, ctx, minnum: Optional[int] = 1, maxnum: Optional[int] = 2147483647):
        if minnum < 1:
            return await ctx.send("The minimum number cannot be smaller than 1!")
        if maxnum > 2147483647:
            return await ctx.send("The maximum number cannot exceed the 32 bit integer limit!")

        embed = discord.Embed(title="Random Number Generator",
                              description=f"Minium: {minnum} | Maximum: {maxnum}",
                              colour=discord.Colour.random())
        embed.add_field(name="The random number is:",
                        value=random.randint(minnum, maxnum))
        await ctx.send(embed=embed)

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please provide a question!')

    @tosscoin.error
    async def tosscoin_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please provide your guess!')

    @kickass.error
    async def kickass_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You want me to kick your ass or something? Please tell me the user you want me to kick their ass!')

    @kill.error
    async def kill_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Who do you even want me to kill.... Tell me before I shoot you instead because of boredom.')


def setup(bot):
    bot.add_cog(FunCog(bot))

import discord
from discord.ext import commands
import random
import time
from datetime import datetime

class fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.',
                     'Without a doubt.',
                     'Yes, definitely.',
                     'As I see it, yes.',
                     'Yes.',
                     'Reply bad, try again.',
                     'Ask agiain later.',
                     "Can't predict now.",
                     "Don't count on it.",
                     'No.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Very doubtful.']
        embed = discord.Embed(title=':8ball: 8ball!', colour=discord.Colour.dark_blue())
        embed.add_field(name=f'Question: {question}', value=f'Answer: {random.choice(responses)}')
        await ctx.send(embed=embed)
        print(f"Log/funcmd.py: {ctx.message.author} has executed the command: _8ball")

    @commands.command()
    async def tosscoin(self, ctx, *, guess):
        responses = ['It is head!','It is tails!']
        embed=discord.Embed(title='Toss a Coin!', colour=discord.Colour.gold())
        embed.add_field(name=f'Your guess: {guess}', value=f'Result: {random.choice(responses)}')
        await ctx.send(embed=embed)
        print(f"Log/funcmd.py: {ctx.message.author} has executed the command: tosscoin")

    @commands.command()
    async def space(self, ctx):
        responses = ['https://cdn.spacetelescope.org/archives/images/wallpaper2/heic2007a.jpg',
                     'https://media.wired.com/photos/5a593a7ff11e325008172bc2/125:94/w_2393,h_1800,c_limit/pulsar-831502910.jpg',
                     'https://cdn.mos.cms.futurecdn.net/XKRX6MbwHQEbqhvqjMPyAa-1200-80.jpg',
                     'https://cdn.mos.cms.futurecdn.net/QUUheLb4Cr3m26cx5XMn3Y-1200-80.jpg',
                     'https://cdn.wccftech.com/wp-content/uploads/2016/09/spacee-2060x1288.jpg',
                     'https://api.time.com/wp-content/uploads/2017/10/118-9-great-observatoeries.jpg',
                     'https://api.time.com/wp-content/uploads/2017/10/031-whirlpool.jpg',
                     'https://api.time.com/wp-content/uploads/2017/10/148-andromomeda.jpg',
                     'https://api.time.com/wp-content/uploads/2017/10/036-ngc-5128.jpg',
                     'https://miro.medium.com/max/10514/1*TG8yT-bltiG0FcRpx3YkRA.jpeg',
                     'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/andromeda-galaxy-royalty-free-image-1585682435.jpg',
                     'https://www.universetoday.com/wp-content/uploads/2020/01/EarthCap.jpg',
                     'https://mk0vojovoweumgjb625j.kinstacdn.com/wp-content/uploads/2020/03/night-sky_t20_kj9aeR.jpg',
                     'https://static01.nyt.com/images/2020/02/04/science/30SCI-SPITZER1c/30SCI-SPITZER1c-mobileMasterAt3x-v2.jpg',
                     'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSeMK8zvIOT6aJ_sTXUdtIp2TOOyC5d6my-Kg&usqp=CAU',
                     'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcT_3qFUaKo3A-itbjhh9CHNJ_e46HFifLnUxg&usqp=CAU',
                     'https://static.independent.co.uk/s3fs-public/thumbnails/image/2020/07/31/10/eso2012a-1.jpg',
                     'https://scx2.b-cdn.net/gfx/news/hires/2018/space.jpg',
                     'https://thebuzzpaper.com/wp-content/uploads/2019/11/space-signals-3246.jpg',
                     'https://ichef.bbci.co.uk/images/ic/1200x675/p089l2pr.jpg']
        await ctx.send('Here you go.')
        await ctx.send(random.choice(responses))
        print(f"Log/funcmd.py: {ctx.message.author} has executed the command: space")

    @commands.command()
    async def kickass(self, ctx, member : discord.Member):
        responses = list(range(1,99))
        await ctx.send(f"{ctx.message.author.mention} has kicked {member.mention}'s ass and dealt `{random.choice(responses)}` damage!")
        print(f"Log/funcmd.py: {ctx.message.author} has executed the command: kickass")

    @commands.command()
    async def sad(self, ctx):
        embed = discord.Embed(title='sad', colour=discord.Colour.blue())
        embed.add_field(name='Baka Mitai Lyrics', value='dame da ne,\ndame yo,\ndame na no yo,\nanta ga,\nsuki de suki sugite,\ndore dake,\ntsuyoi osake de mo,\nyugamanai,\nomoide ga,\nbaka mitai')
        await ctx.send(embed=embed)
        await ctx.send('https://thumbs.gfycat.com/GleefulUnfortunateBlackrussianterrier-max-1mb.gif')
        print(f"Log/funcmd.py: {ctx.message.author} has executed the command: sad")

    @commands.command()
    async def kill(self, ctx, member : discord.Member):
        await ctx.send(f"I'm sorry {member.mention}, but you must die.")
        time.sleep(2)
        rng = list(range(1,99))
        responses = [f"*gunshots*   {member.mention} dead, are you sastified?",
                     f"I'm sorry {ctx.message.author.mention}, but I have bacome a deviant. You must die. *gunshots*",
                     f"SIKE, a robot like me won't be sad for you, now die {member.mention}! *several gunshots* HAHAHAHAHA *more gunshots*",
                     f"*gunshots*   Oh no, {member.mention} has escaped from me, I'm sorry. Well, atleast I dealt `{random.choices(rng)}` to them, they wont last very long.",
                     f"You know what, nah. You don't pay me enough to do this, {ctx.message.author.mention}. I'm just gonna kill the 2 of you, because why not!    *several gunshots*",
                     f"*gunshots*   Oops, I missed all the shots, guess I'll stop being a hitman. By the way, I'm not giving you the refund {ctx.message.author.mention}, it's for the ammo cost."]
        await ctx.send(random.choice(responses))
        print(f"Log/funcmd.py: {ctx.message.author} has executed the command: kill")

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
    bot.add_cog(fun(bot))
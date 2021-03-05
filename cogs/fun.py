import asyncio
import random
from datetime import datetime
from typing import Optional

import aiofiles
import aiosqlite
import discord
from discord.ext import commands


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


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball", aliases=["8b", "eightball"], help="Ask the 8 ball and it will answer you.")
    @commands.before_invoke(verification_channel_check)
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
    @commands.before_invoke(verification_channel_check)
    async def tosscoin(self, ctx, *, guess):
        responses = ['It is head!', 'It is tails!']
        embed = discord.Embed(title='Toss a Coin!',
                              colour=discord.Colour.gold())
        embed.add_field(
            name=f'Your guess: {guess}', value=f'Result: {random.choice(responses)}')
        await ctx.send(embed=embed)

    @commands.command(help="gBot will send a random picture of space.")
    @commands.before_invoke(verification_channel_check)
    async def space(self, ctx):
        async with aiofiles.open(f"{self.bot.path}/data/space_pictures.txt", "r") as f:
            responses = await f.readlines()
        await ctx.send('Here you go.')
        await ctx.send(random.choice(responses))

    @commands.command(aliases=["ka"], help="Ass kicking' time!")
    @commands.before_invoke(verification_channel_check)
    async def kickass(self, ctx, member: discord.Member):
        responses = list(range(1, 99))
        await ctx.send(f"{ctx.message.author.mention} has kicked {member.mention}'s ass and dealt `{random.choice(responses)}` damage!")

    @commands.command(help="gBot will **try** to kill the user.")
    @commands.before_invoke(verification_channel_check)
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
    @commands.before_invoke(verification_channel_check)
    async def httpcode(self, ctx, http_code: Optional[int] = None):
        async with aiofiles.open(f"{self.bot.path}/data/http.txt", "r") as f:
            responses = await f.readlines()
        embed = discord.Embed()
        embed.set_image(url=random.choice(responses))
        embed.set_footer(text="Images taken from: https://http.cat")
        await ctx.send(embed=embed)

    @commands.command(help="gBot will generate a random number between 1 and 2,147,483,647 if not specified.")
    @commands.before_invoke(verification_channel_check)
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

    @commands.command(help="gBot will generate an embed. This command is interactive.")
    @commands.before_invoke(verification_channel_check)
    async def createembed(self, ctx):
        user_id = ctx.author.id
        embed = {}
        embed_color = {}
        embed_init = {}
        embed_title = {}
        embed_desc = {}
        number_of_fields = {}
        is_inline = {}
        embed_author = {}
        embed_footer = {}
        embed_thumbnail = {}
        embed_image = {}

        try:
            if embed_color[user_id]:
                return await ctx.send("You're already trying to create an embed! Please finish creating that one first.")
        except KeyError: pass

        await ctx.send("What do you want the color of the embed to be? Please provide a hex number, also don't forget the hash.")
        embed_color[user_id] = await self.bot.wait_for("message", timeout=30, check=lambda message: message.author == ctx.author)
        try:
            embed_color[user_id] = embed_color[user_id].content
            embed_color[user_id] = await commands.ColourConverter().convert(ctx, embed_color.get(user_id))
        except commands.CommandError:
            embed_color.pop(user_id)
            return await ctx.send("That hex value is not a valid color! Please try again.")

        await ctx.send("What do you want the title and the description of the embed to be? Split them using `|`. If you only provide one value, the title will be set.")
        try:
            embed_init[user_id] = await self.bot.wait_for("message", timeout=180, check=lambda message: message.author == ctx.author)
            try:
                embed_title[user_id], embed_desc[user_id] = embed_init[user_id].content.split("|")
                embed[user_id] = discord.Embed(title=embed_title.get(user_id),
                                               description=embed_desc.get(user_id),
                                               colour=embed_color.get(user_id))
                await ctx.send(f"Nice! So the title is `{embed_title.get(user_id)}` and the description is `{embed_desc.get(user_id)}`.")
            except ValueError:
                embed[user_id] = discord.Embed(title=embed_init[user_id].content,
                                               colour=embed_color.get(user_id))
                await ctx.send(f"Nice! So the title is {embed_init[user_id].content}")

            await ctx.send("Now, how many fields do you want in the embed? The maximum number is `12`.")
            number_of_fields[user_id] = await self.bot.wait_for("message", timeout=30, check=lambda message: message.author == ctx.author)
            try:
                number_of_fields[user_id] = int(number_of_fields[user_id].content)
                if number_of_fields.get(user_id) > 12:
                    embed.pop(user_id)
                    embed_color.pop(user_id)
                    embed_init.pop(user_id)
                    try:
                        embed_title.pop(user_id)
                        embed_desc.pop(user_id)
                    except KeyError: pass
                    number_of_fields.pop(user_id)
                    return await ctx.send("The number of fields you provided is more than `12`! Please try again.")

                await ctx.send(f"Alright! So the number of fields you want is `{number_of_fields.get(user_id)}`. Do you want them to be inline? Please respond with `yes` or `no`.")
            except ValueError:
                embed.pop(user_id)
                embed_color.pop(user_id)
                embed_init.pop(user_id)
                try:
                    embed_title.pop(user_id)
                    embed_desc.pop(user_id)
                except KeyError: pass
                number_of_fields.pop(user_id)
                return await ctx.send("That is not a number! Please try again.")

            is_inline[user_id] = await self.bot.wait_for("message", timeout=15, check=lambda message: message.author == ctx.author)
            if is_inline[user_id].content.lower() == "yes":
                is_inline[user_id] = True
                await ctx.send("So you want the fields to be inline, noted.")
            elif is_inline[user_id].content.lower() == "no":
                is_inline[user_id] = False
                await ctx.send("So you don't want the fields to be inline, noted.")
            else:
                embed.pop(user_id)
                embed_color.pop(user_id)
                embed_init.pop(user_id)
                try:
                    embed_title.pop(user_id)
                    embed_desc.pop(user_id)
                except KeyError: pass
                number_of_fields.pop(user_id)
                is_inline.pop(user_id)
                return await ctx.send("That is not a valid option! Please try again.")

            for i in range(number_of_fields.get(user_id)):
                await ctx.send(f"What do you want the heading and the content of field `{i + 1}` to be? Split them using `|`.")
                heading = {}
                content = {}
                field_value = await self.bot.wait_for("message", timeout=180, check=lambda message: message.author == ctx.author)
                heading[user_id], content[user_id] = field_value.content.split("|")
                embed[user_id].add_field(name=heading.get(user_id),
                                         value=content.get(user_id),
                                         inline=is_inline.get(user_id))
                heading.pop(user_id)
                content.pop(user_id)
            
            await ctx.send("Alright, we're almost done! The next step is to provide me the content of the author field, it is at the top of an embed. The options you can provide are the content and the icon url. Split them using `|`. The content is required but the icon url is optional. Type `skip` to skip.")
            embed_author[user_id] = await self.bot.wait_for("message", timeout=60, check=lambda message: message.author == ctx.author)
            if embed_author[user_id].content.lower == "skip":
                await ctx.send("Skipped!")
            else:
                print(embed_author[user_id].content.lower)
                embed_author_content, embed_author_icon = embed_author[user_id].content.split("|")
                embed[user_id].set_author(name=embed_author_content,
                                          icon_url=embed_author_icon)
            
            await ctx.send("Now we need to set the footer. It's the same as the author field, but it's at the bottom. The options are the same. Type `skip` to skip.")
            embed_footer[user_id] = await self.bot.wait_for("message", timeout=60, check=lambda message: message.author == ctx.author)
            if embed_footer[user_id].content.lower == "skip":
                await ctx.send("Skipped!")
            else:
                embed_footer_content, embed_footer_icon = embed_footer[user_id].content.split("|")
                embed[user_id].set_footer(text=embed_footer_content,
                                          icon_url=embed_footer_icon)

            await ctx.send("Now you need to provide the url for the thumbnail. It will be located in the top-right of the embed. Type `skip` to skip.")
            embed_thumbnail[user_id] = await self.bot.wait_for("message", timeout=30, check=lambda message: message.author == ctx.author)
            if embed_thumbnail[user_id].content.lower == "skip":
                await ctx.send("Skipped!")
            else:
                embed[user_id].set_thumbnail(url=embed_thumbnail[user_id].content)
            
            await ctx.send("Last step! You need to provide the embed image url. It will be located below all the fields. Type `skip` to skip.")
            embed_image[user_id] = await self.bot.wait_for("message", timeout=30, check=lambda message: message.author == ctx.author)
            if embed_image[user_id].content.lower == "skip":
                await ctx.send("Skipped!")
            else:
                embed[user_id].set_image(url=embed_image[user_id].content)

            await ctx.send(embed=embed.get(user_id))
            embed.pop(user_id)
            embed_color.pop(user_id)
            embed_init.pop(user_id)
            try:
                embed_title.pop(user_id)
                embed_desc.pop(user_id)
            except KeyError: pass
            number_of_fields.pop(user_id)
            is_inline.pop(user_id)
            embed_author.pop(user_id)
            embed_footer.pop(user_id)
            embed_thumbnail.pop(user_id)
            embed_image.pop(user_id)
        except asyncio.TimeoutError:
            await ctx.send("You took too long. Please try again.")

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

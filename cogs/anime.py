import random
from typing import Optional

import aiohttp
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


class AnimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dbpath = self.bot.dbpath
        self.sfw_categories = ["waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug", "awoo", "kiss",
                               "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold",
                               "nom", "bite", "glomp", "kill", "slap", "happy", "wink", "poke", "dance", "cringe"]
        self.nsfw_categories = ["waifu", "neko", "trap", "blowjob"]

    @commands.group(help="Sends a random waifu picture if a category or type is not provided.")
    @commands.cooldown(rate=1, per=5, type=commands.cooldowns.BucketType.user)
    @commands.before_invoke(verification_channel_check)
    async def waifu(self, ctx):
        if ctx.invoked_subcommand is None:
            async with aiohttp.ClientSession() as cs:
                waifu_picture = (await (await cs.get(f"https://waifu.pics/api/sfw/{random.choice(self.sfw_categories)}")).json())

                embed = discord.Embed(title="Here you go!")
                embed.set_author(name=f"To see all the categories, type \"{await self.bot.get_prefix(ctx.message)}waifu categories\".")
                embed.set_image(url=waifu_picture["url"])
                embed.set_footer(text="Thanks to waifu.pics for these amazing pictures!")

                await ctx.send(embed=embed)

    @waifu.command(help="List all of the waifu pictures categories.")
    @commands.cooldown(rate=1, per=5, type=commands.cooldowns.BucketType.user)
    @commands.before_invoke(verification_channel_check)
    async def categories(self, ctx):
        sfw = ""
        nsfw = ""

        for i in range(len(self.sfw_categories)):
            sfw += f"{self.sfw_categories[i]}\n"
        for j in range(len(self.nsfw_categories)):
            nsfw += f"{self.nsfw_categories[i]}\n"

        embed = discord.Embed(title="Waifu Categories")
        embed.add_field(name="SFW Categories:", value=sfw)
        embed.add_field(name="NSFW Categories:", value=nsfw)
        embed.set_footer(text="Note: NSFW Categories can only be used in nsfw channels.")

        await ctx.send(embed=embed)
    
    @waifu.command(help="Sends a random SFW waifu picture if a category is not provided.")
    @commands.cooldown(rate=1, per=5, type=commands.cooldowns.BucketType.user)
    @commands.before_invoke(verification_channel_check)
    async def sfw(self, ctx, category: Optional[str] = None):
        if not category:
            async with aiohttp.ClientSession() as cs:
                waifu_picture = (await (await cs.get(f"https://waifu.pics/api/sfw/{random.choice(self.sfw_categories)}")).json())

                embed = discord.Embed(title="Here you go!")
                embed.set_image(url=waifu_picture["url"])
                embed.set_footer(text="Thanks to waifu.pics for these amazing pictures!")

                return await ctx.send(embed=embed)

        if category.lower() not in self.sfw_categories:
            return await ctx.send(f"`{category.lower()}` is not a valid category! Use `{await self.bot.get_prefix(ctx.message)}waifu categories` to see all avaliable categories.")

        async with aiohttp.ClientSession() as cs:
            waifu_picture = (await (await cs.get(f"https://waifu.pics/api/sfw/{category.lower()}")).json())

            embed = discord.Embed(title="Here you go!", description=f"Category: {category.lower()}")
            embed.set_image(url=waifu_picture["url"])
            embed.set_footer(text="Thanks to waifu.pics for these amazing pictures!")

            return await ctx.send(embed=embed)
    
    @waifu.command(help="Sends a random NSFW waifu picture if a category is not provided. This command can only be used in NSFW channels.")
    @commands.is_nsfw()
    @commands.cooldown(rate=1, per=5, type=commands.cooldowns.BucketType.user)
    @commands.before_invoke(verification_channel_check)
    async def nsfw(self, ctx, category: Optional[str] = None):
        if not category:
            async with aiohttp.ClientSession() as cs:
                waifu_picture = (await (await cs.get(f"https://waifu.pics/api/nsfw/{random.choice(self.nsfw_categories)}")).json())

                embed = discord.Embed(title="Here you go!")
                embed.set_image(url=waifu_picture["url"])
                embed.set_footer(text="Thanks to waifu.pics for these amazing pictures!")

                return await ctx.send(embed=embed)

        if category.lower() not in self.nsfw_categories:
            return await ctx.send(f"`{category.lower()}` is not a valid category! Use `{await self.bot.get_prefix(ctx.message)}waifu categories` to see all avaliable categories.")

        async with aiohttp.ClientSession() as cs:
            waifu_picture = (await (await cs.get(f"https://waifu.pics/api/nsfw/{category.lower()}")).json())

            embed = discord.Embed(title="Here you go!", description=f"Category: {category.lower()}")
            embed.set_image(url=waifu_picture["url"])
            embed.set_footer(text="Thanks to waifu.pics for these amazing pictures!")

            return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AnimeCog(bot))

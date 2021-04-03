import asyncio
import os
import random
from datetime import datetime
from typing import Optional

import aiosqlite
import discord
from captcha.image import ImageCaptcha
from discord.ext import commands


def AsyncImageCaptcha(chars, output):
    return ImageCaptcha().write(chars, output)


def generate_captcha_content():
    captcha_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                     'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    number_captcha_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    captcha_content = []
    for i in range(6):
        randomizer = random.randint(1, 4)
        if randomizer in [1, 2, 3]:
            captcha_content.append(random.choice(captcha_chars))
        else:
            captcha_content.append(random.choice(number_captcha_chars))
    return captcha_content


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


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dbpath = self.bot.dbpath

    @commands.command(aliases=["purge", "cls", "delete", "remove"], help="gBot will clear messages.")
    @commands.before_invoke(verification_channel_check)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int, member: commands.MemberConverter = None):
        if member:
            await ctx.channel.purge(
                limit=amount,
                check=lambda message: message.author.id == member.id
            )
            await ctx.send(f"Cleared `{amount}` messages from {member.name}.", delete_after=1)
        else:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"Cleared `{amount}` messages.", delete_after=1)

    @commands.command(help="gBot will mute a user.")
    @commands.before_invoke(verification_channel_check)
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: commands.MemberConverter, *, reason: Optional[str] = None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        perms = discord.Permissions()
        perms.update(
            send_messages=False,
            read_message_history=True,
            read_messages=True
        )
        if not role:
            muted = await ctx.guild.create_role(name="Muted", reason=None)
            await muted.edit(permissions=perms)
            role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        await ctx.send(f'{member.mention} has been muted. Reason: {reason}')

    @commands.command(help="gBot will unmute a user.")
    @commands.before_invoke(verification_channel_check)
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: commands.MemberConverter):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(role)
        await ctx.send(f'{member.mention} has been unmuted.')

    @commands.command(help="gBot will kick a user.")
    @commands.before_invoke(verification_channel_check)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason: Optional[str] = None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has beed kicked. Reason: {reason}')

    @commands.command(help="gBot will ban a user.")
    @commands.before_invoke(verification_channel_check)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason: Optional[str] = None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has beed banned. Reason: {reason}')

    @commands.command(help="gBot will unban a user.")
    @commands.before_invoke(verification_channel_check)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} has been unbanned.')
            return

    @commands.command(help="gBot will send you a captcha to verify that you're not a robot.")
    async def verify(self, ctx):
        user_id = ctx.author.id
        async with aiosqlite.connect(self.dbpath) as db:
            async with db.execute("""SELECT captcha_channel_id FROM guild_config WHERE guild_id=?""", (ctx.guild.id,)) as cursor:
                captcha_channel_id = await cursor.fetchone()
                if ctx.channel.id != int(captcha_channel_id[0]):
                    return await ctx.send(f"This command can only be used in a verification channel. If you're an admin and have not set a verification channel, use the command `{await self.bot.get_prefix(ctx.message)}setverificationchannel`")

        loop = asyncio.get_running_loop()
        captcha_content = {}
        captcha_content[user_id] = "".join(generate_captcha_content())
        captcha_img = await loop.run_in_executor(None, AsyncImageCaptcha, captcha_content[user_id], f"{self.bot.path}/data/captcha-{user_id}.png")
        captcha_img = discord.File(f"{self.bot.path}/data/captcha-{user_id}.png", filename=f"captcha-{user_id}.png")

        embed = discord.Embed()
        embed.set_image(url=f"attachment://captcha-{user_id}.png")
        embed.set_footer(text="Please type the captcha above in **uppercase**. Timeout: 20 Seconds")

        msg = await ctx.send(file=captcha_img, embed=embed)
        try:
            captcha_check = await self.bot.wait_for(
                "message",
                timeout=20,
                check=lambda message: message.author == ctx.author
            )
            if captcha_check.content == captcha_content[user_id]:
                os.remove(f"{self.bot.path}/data/captcha-{user_id}.png")
                captcha_content.pop(user_id)
                await ctx.message.delete()
                await msg.delete()
                await captcha_check.delete()
                await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name="Verified"))
                return await ctx.send(":white_check_mark: You are now verified!", delete_after=2)
            else:
                os.remove(f"{self.bot.path}/data/captcha-{user_id}.png")
                captcha_content.pop(user_id)
                await ctx.message.delete()
                await msg.delete()
                await captcha_check.delete()
                return await ctx.send(":x: Captcha verification failed. Please try again.", delete_after=2)
        except asyncio.exceptions.TimeoutError:
            os.remove(f"{self.bot.path}/data/captcha-{user_id}.png")
            captcha_content.pop(user_id)
            await ctx.message.delete()
            await msg.delete()
            return await ctx.send(":x: Took too long. Please try again.", delete_after=2)


def setup(bot):
    bot.add_cog(ModCog(bot))

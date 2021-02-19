import asyncio
from datetime import datetime
from typing import Optional

import discord
from discord.ext import commands
from gServerTools import infolog

class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id == 786180842862018570:
            bad = ["hey language","language","lαnguage","ianguage"]
            for word in bad:
                if word in message.content.lower():
                    await message.delete()
                    await message.channel.send("Oi mate the l-word is restricted here")
        else:
            pass


    @commands.command(aliases=["purge", "cls", "delete", "remove"], help="gBot will clear messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        amount = amount + 1
        await ctx.channel.purge(limit=amount)
        notify = await ctx.send(f"Cleared `{amount-1}` messages.")
        await asyncio.sleep(1)
        await notify.delete()
        infolog(f"{ctx.message.author} has executed the command: clear")

    @commands.command(help="gBot will mute a user.")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason: Optional[str] = None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        perms = discord.Permissions()
        perms.update(send_messages=False, read_message_history=True, read_messages=True)
        if not role:
            muted = await ctx.guild.create_role(name="Muted", reason=None)
            await muted.edit(permissions=perms)
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        await ctx.send(f'{member.mention} has been muted. Reason: {reason}')
        infolog(f"{ctx.message.author} has executed the command: mute")

    @commands.command(help="gBot will unmute a user.")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(role)
        await ctx.send(f'{member.mention} has been unmuted.')
        infolog(f"{ctx.message.author} has executed the command: unmute")

    @commands.command(help="gBot will kick a user.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: Optional[str] = None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has beed kicked. Reason: {reason}')
        infolog(f"{ctx.message.author} has executed the command: kick")

    @commands.command(help="gBot will ban a user.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: Optional[str] = None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has beed banned. Reason: {reason}')
        infolog(f"{ctx.message.author} has executed the command: ban")

    @commands.command(help="gBot will unban a user.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} has been unbanned.')
            infolog(f"{ctx.message.author} has executed the command: unban")
            return

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please provide the number of messages you want to clear.')

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me the person you want to mute.')

    @unmute.error
    async def unmute_error(self, ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me the person you want to unmute.')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me the person you want to kick.')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me the person you want to ban.')

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me the person you want to unban.')


def setup(bot):
    bot.add_cog(ModCog(bot))

import time
from datetime import datetime

import discord
from discord.ext import commands


class mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        amount = amount + 1
        await ctx.channel.purge(limit=amount)
        notify = await ctx.send(f"Cleared `{amount-1}` messages.")
        time.sleep(1)
        await notify.delete()
        print(f"Log/modcmd.py: {ctx.message.author} has executed the command: clear")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member : discord.Member, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        perms = discord.Permissions()
        perms.update(send_messages=False, read_message_history=True, read_messages=True)
        if not role:
            muted = await ctx.guild.create_role(name="Muted", reason=None)
            await muted.edit(permissions=perms)
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        await ctx.send(f'{member.mention} has been muted. Reason: {reason}')
        print(f"Log/modcmd.py: {ctx.message.author} has executed the command: mute")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member : discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(role)
        await ctx.send(f'{member.mention} has been unmuted.')
        print(f"Log/modcmd.py: {ctx.message.author} has executed the command: unmute")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has beed kicked.')
        print(f"Log/modcmd.py: {ctx.message.author} has executed the command: kick")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has beed banned.')
        print(f"Log/modcmd.py: {ctx.message.author} has executed the command: ban")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} has been unbanned.')
            print(f"Log/modcmd.py: {ctx.message.author} has executed the command: unban")
            return

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please provide the number of messages you want to clear.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, but you don't have permissions to do that.")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me the person you want to mute.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, but you don't have permissions to do that.")

    @unmute.error
    async def unmute_error(self, ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me the person you want to unmute.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, but you don't have permissions to do that.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me the person you want to kick.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, but you don't have permissions to do that.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me the person you want to ban.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, but you don't have permissions to do that.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me the person you want to unban.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Sorry, but you don't have the permissions to do that.")

def setup(bot):
    bot.add_cog(mod(bot))

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


class ConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dbpath = self.bot.dbpath

    @commands.command(help="Set gBot's prefix for this server. Only admins can do this.")
    @commands.before_invoke(verification_channel_check)
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, pref):
        async with aiosqlite.connect(self.dbpath) as db:
            await db.execute("""UPDATE guild_config SET prefix=? WHERE guild_id=?""", (pref, ctx.guild.id))
            await db.commit()
            await ctx.send(f"Server prefix successfully changed to `{pref}`.")

    @commands.command(help="See gBot's prefix for this server.")
    @commands.before_invoke(verification_channel_check)
    async def prefix(self, ctx):
        async with aiosqlite.connect(self.dbpath) as db:
            async with db.execute("""SELECT prefix FROM guild_config WHERE guild_id=?""", (ctx.guild.id,)) as cursor:
                pref = await cursor.fetchone()
                await ctx.send(f"The prefix for this server is `{pref[0]}`.")

    @commands.command(help="Set gBot's pagination mode for this server. `manual` mode will not remove reactions automatically and will not delete messages. `auto` mode does the opposite. Only admins can do this.")
    @commands.before_invoke(verification_channel_check)
    @commands.has_permissions(administrator=True)
    async def setpaginationmode(self, ctx, mode: str):
        if (mode.lower() == "manual") or (mode.lower() == "auto"):
            async with aiosqlite.connect(self.dbpath) as db:
                await db.execute("""UPDATE guild_config SET pagination=? WHERE guild_id=?""", (mode.lower(), ctx.guild.id))
                await db.commit()
                return await ctx.send(f"Pagination mode successfully changed to `{mode}`.")
        else:
            return await ctx.send(f"`{mode}` is not a valid mode. Valid modes are: `manual` and `auto`.")

    @commands.command(help="See gBot's pagination mode for this server.")
    @commands.before_invoke(verification_channel_check)
    async def paginationmode(self, ctx):
        async with aiosqlite.connect(self.dbpath) as db:
            async with db.execute("""SELECT pagination FROM guild_config WHERE guild_id=?""", (ctx.guild.id,)) as cursor:
                mode = await cursor.fetchone()
                await ctx.send(f"The pagination mode for this server is `{mode[0]}`.")

    @commands.command(help="Set gBot's captcha verification channel and also restrict everyone from accessing other channels if they're not verified. Verified people get the 'Verified' role. Only admins can do this.")
    @commands.before_invoke(verification_channel_check)
    @commands.has_permissions(administrator=True)
    async def setverificationchannel(self, ctx, *, verification_channel: commands.TextChannelConverter):
        async with aiosqlite.connect(self.dbpath) as db:
            await db.execute("""UPDATE guild_config SET captcha_channel_id=? WHERE guild_id=?""", (verification_channel.id, ctx.guild.id))
            await db.commit()
            await ctx.send(f"Verification channel successfully changed to <#{verification_channel.id}>.")
        perms = discord.Permissions()
        perms.update(
            view_channel=True,
            change_nickname=True,
            send_messages=True,
            embed_links=True,
            attach_files=True,
            add_reactions=True,
            use_external_emojis=True,
            read_message_history=True,
            use_slash_commands=True,
            connect=True,
            speak=True,
            stream=True,
            use_voice_activation=True,
            read_messages=True
        )
        verified_role = discord.utils.get(ctx.guild.roles, name="Verified")
        if not verified_role:
            await (
                await ctx.guild.create_role(name="Verified")
            ).edit(permissions=perms)
            verified_role = discord.utils.get(ctx.guild.roles, name="Verified")

        for channel in ctx.guild.channels:
            if channel.id == verification_channel.id:
                await channel.edit(overwrites={
                    ctx.guild.default_role: discord.PermissionOverwrite(
                        view_channel=True
                    ),
                    verified_role: discord.PermissionOverwrite(
                        view_channel=False
                    )
                })
                embed = discord.Embed(
                    title=f"Welcome to ***{ctx.guild.name}***!",
                    description="Please verify yourself to get access to the rest of the server.",
                    color=discord.Colour.blurple()
                )
                embed.add_field(
                    name="How to verify:",
                    value=f"Just type `{await self.bot.get_prefix(ctx.message)}verify`, then wait for te bot to send the captcha. After that, complete the captcha and you will be verified!"
                )
                await channel.send(embed=embed)
            else:
                await channel.edit(overwrites={
                    ctx.guild.default_role: discord.PermissionOverwrite(
                        view_channel=False
                    ),
                    verified_role: discord.PermissionOverwrite(
                        view_channel=True
                    )
                })

    @commands.command(help="see gBot's verification channel for this server.")
    @commands.before_invoke(verification_channel_check)
    async def verificationchannel(self, ctx):
        async with aiosqlite.connect(self.dbpath) as db:
            async with db.execute("""SELECT captcha_channel_id FROM guild_config WHERE guild_id=?""", (ctx.guild.id,)) as cursor:
                channel = await cursor.fetchone()
                await ctx.send(f"The verification channel for this server is <#{channel[0]}>.")


def setup(bot):
    bot.add_cog(ConfigCog(bot))

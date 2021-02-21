import aiosqlite
from discord.ext import commands

from gServerTools import infolog


class ConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dbpath = self.bot.dbpath

    @commands.command(help="Set gBot's prefix for this server. Only admins can do this.")
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, pref):
        async with aiosqlite.connect(self.dbpath) as db:
            await db.execute("""UPDATE guild_config SET prefix=? WHERE guild_id=?""", (pref, ctx.guild.id))
            await db.commit()
            await ctx.send(f"Server prefix successfully changed to `{pref}`.")

    @commands.command(help="See gBot's prefix for this server.")
    async def prefix(self, ctx):
        async with aiosqlite.connect(self.dbpath) as db:
            async with db.execute("""SELECT prefix FROM guild_config WHERE guild_id=?""", (ctx.guild.id,)) as cursor:
                pref = await cursor.fetchone()
                await ctx.send(f"The prefix for this server is `{pref[0]}`.")

    @commands.command(help="Set gBot's pagination mode for this server Only admins can do this.")
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
    async def paginationmode(self, ctx):
        async with aiosqlite.connect(self.dbpath) as db:
            async with db.execute("""SELECT pagination FROM guild_config WHERE guild_id=?""", (ctx.guild.id,)) as cursor:
                mode = await cursor.fetchone()
                await ctx.send(f"The pagination mode for this server is `{mode[0]}`.")


def setup(bot):
    bot.add_cog(ConfigCog(bot))

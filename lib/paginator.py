import asyncio

class Paginator():
    def __init__(self, bot, contents, pages, ctx):
        super().__init__()
        self.bot = bot
        self.contents = contents
        self.pages = pages
        self.cur_page = 1
        self.ctx = ctx

    async def start_full(self):
        message = await self.ctx.send(embed=(self.contents[self.cur_page - 1]))

        await message.add_reaction("⏪")
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("⏩")
        await message.add_reaction("⏹️")

        def check(reaction, user):
            return user == self.ctx.author and str(
                reaction.emoji) in ["⏪", "◀️", "▶️", "⏩", "⏹️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "⏪" and self.cur_page > 1:
                    self.cur_page = 1
                    await message.edit(embed=(self.contents[self.cur_page - 1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and self.cur_page > 1:
                    self.cur_page -= 1
                    await message.edit(embed=(self.contents[self.cur_page - 1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "▶️" and self.cur_page != self.pages:
                    self.cur_page += 1
                    await message.edit(embed=(self.contents[self.cur_page - 1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏩" and self.cur_page != self.pages:
                    self.cur_page = self.pages
                    await message.edit(embed=(self.contents[self.cur_page - 1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏹️":
                    await self.ctx.message.delete()
                    await message.delete()
                    break

                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await self.ctx.message.delete()
                await message.delete()
                break

    async def start_simple(self):
        message = await self.ctx.send(embed=(self.contents[self.cur_page - 1]))

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("⏹️")

        def check(reaction, user):
            return user == self.ctx.author and str(
                reaction.emoji) in ["◀️", "▶️", "⏹️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "◀️" and self.cur_page > 1:
                    self.cur_page -= 1
                    await message.edit(embed=(self.contents[self.cur_page - 1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "▶️" and self.cur_page != self.pages:
                    self.cur_page += 1
                    await message.edit(embed=(self.contents[self.cur_page - 1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏹️":
                    await self.ctx.message.delete()
                    await message.delete()
                    break

                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await self.ctx.message.delete()
                await message.delete()
                break
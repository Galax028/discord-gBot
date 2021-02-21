import asyncio

from discord.ext import commands


class Paginator():
    def __init__(self, bot, contents, pages, ctx, user_id):
        super().__init__()
        self.bot = bot
        self.contents = {}
        self.pages = {}
        self.cur_page = {}
        self.ctx = ctx
        self.user_id = user_id

        self.contents[user_id] = contents
        self.cur_page[user_id] = 1
        self.pages[user_id] = pages

    async def start_full(self):
        message = await self.ctx.send(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))

        await message.add_reaction("⏪")
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("⏩")
        await message.add_reaction("⏹️")

        def check(reaction, user):
            return user == self.ctx.author and str(reaction.emoji) in ["⏪", "◀️", "▶️", "⏩", "⏹️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "⏪" and self.cur_page[self.user_id] > 1:
                    self.cur_page[self.user_id] = 1
                    await message.edit(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and self.cur_page[self.user_id] > 1:
                    self.cur_page[self.user_id] -= 1
                    await message.edit(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "▶️" and self.cur_page[self.user_id] != self.pages[self.user_id]:
                    self.cur_page[self.user_id] += 1
                    await message.edit(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏩" and self.cur_page[self.user_id] != self.pages[self.user_id]:
                    self.cur_page[self.user_id] = self.pages[self.user_id]
                    await message.edit(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏹️":
                    await self.ctx.message.delete()
                    await message.delete()
                    self.contents.pop(self.user_id)
                    self.cur_page.pop(self.user_id)
                    self.pages.pop(self.user_id)
                    break

                else:
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                await self.ctx.message.delete()
                await message.delete()
                self.contents.pop(self.user_id)
                self.cur_page.pop(self.user_id)
                self.pages.pop(self.user_id)
                break

    async def start_simple(self):
        message = await self.ctx.send(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("⏹️")

        def check(reaction, user):
            return user == self.ctx.author and str(reaction.emoji) in ["◀️", "▶️", "⏹️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "◀️" and self.cur_page[self.user_id] > 1:
                    self.cur_page[self.user_id] -= 1
                    await message.edit(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "▶️" and self.cur_page[self.user_id] != self.pages[self.user_id]:
                    self.cur_page[self.user_id] += 1
                    await message.edit(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⏹️":
                    await self.ctx.message.delete()
                    await message.delete()
                    self.contents.pop(self.user_id)
                    self.cur_page.pop(self.user_id)
                    self.pages.pop(self.user_id)
                    break

                else:
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                await self.ctx.message.delete()
                await message.delete()
                self.contents.pop(self.user_id)
                self.cur_page.pop(self.user_id)
                self.pages.pop(self.user_id)
                break
    
    async def start_full_manual(self):
        message = await self.ctx.send(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))

        await message.add_reaction("⏪")
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("⏩")
        await message.add_reaction("⏹️")

        def check(reaction, user):
            return user == self.ctx.author and str(reaction.emoji) in ["⏪", "◀️", "▶️", "⏩", "⏹️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "⏪" and self.cur_page[self.user_id] > 1:
                    self.cur_page[self.user_id] = 1
                    await message.edit(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))

                elif str(reaction.emoji) == "◀️" and self.cur_page[self.user_id] > 1:
                    self.cur_page[self.user_id] -= 1
                    await message.edit(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))

                elif str(reaction.emoji) == "▶️" and self.cur_page[self.user_id] != self.pages[self.user_id]:
                    self.cur_page[self.user_id] += 1
                    await message.edit(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))

                elif str(reaction.emoji) == "⏩" and self.cur_page[self.user_id] != self.pages[self.user_id]:
                    self.cur_page[self.user_id] = self.pages[self.user_id]
                    await message.edit(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))

                elif str(reaction.emoji) == "⏹️":
                    for bot_reactions in ["⏪", "◀️", "▶️", "⏩", "⏹️"]:
                        await message.remove_reaction(bot_reactions, self.bot.user)
                    self.contents.pop(self.user_id)
                    self.cur_page.pop(self.user_id)
                    self.pages.pop(self.user_id)
                    break

            except asyncio.TimeoutError:
                for bot_reactions in ["⏪", "◀️", "▶️", "⏩", "⏹️"]:
                        await message.remove_reaction(bot_reactions, self.bot.user)
                self.contents.pop(self.user_id)
                self.cur_page.pop(self.user_id)
                self.pages.pop(self.user_id)
                break

    async def start_simple_manual(self):
        message = await self.ctx.send(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("⏹️")

        def check(reaction, user):
            return user == self.ctx.author and str(reaction.emoji) in ["◀️", "▶️", "⏹️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "◀️" and self.cur_page[self.user_id] > 1:
                    self.cur_page[self.user_id] -= 1
                    await message.edit(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))

                elif str(reaction.emoji) == "▶️" and self.cur_page[self.user_id] != self.pages[self.user_id]:
                    self.cur_page[self.user_id] += 1
                    await message.edit(embed=(self.contents[self.user_id][self.cur_page[self.user_id] - 1]))

                elif str(reaction.emoji) == "⏹️":
                    for bot_reactions in ["◀️", "▶️", "⏹️"]:
                        await message.remove_reaction(bot_reactions, self.bot.user)
                    self.contents.pop(self.user_id)
                    self.cur_page.pop(self.user_id)
                    self.pages.pop(self.user_id)
                    break

            except asyncio.TimeoutError:
                for bot_reactions in ["◀️", "▶️", "⏹️"]:
                    await message.remove_reaction(bot_reactions, self.bot.user)
                self.contents.pop(self.user_id)
                self.cur_page.pop(self.user_id)
                self.pages.pop(self.user_id)
                break

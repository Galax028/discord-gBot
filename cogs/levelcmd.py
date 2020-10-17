import discord
from discord.ext import commands
import json
import random

def read_json():
    with open ("./json_data/levels.json", 'r') as f:
        json_ctx = f.readlines()
        return ' '.join(json_ctx)
levels_json = read_json()

class level(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()    
    async def on_member_join(self, member):
        with open("./json_data/levels.json", 'r') as f:
            users = json.load(f)

        await self.update_data(users, member)

        with open('./json_data/levels.json', 'w') as f:
            json.dump(users, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            with open('./json_data/levels.json', 'r') as f:
                users = json.load(f)

            await self.update_data(users, message.author)
            await self.add_experience(users, message.author, random.randint(10, 20))
            await self.level_up(users, message.author, message)

            with open('./json_data/levels.json', 'w') as f:
                json.dump(users, f)

    async def update_data(self, users, user):
        if not f'{user.id}' in users:
            users[f'{user.id}'] = {}
            users[f'{user.id}']['experience'] = 0
            users[f'{user.id}']['level'] = 1

    async def add_experience(self, users, user, exp):
        users[f'{user.id}']['experience'] += exp

    async def level_up(self, users, user, message):
        global experience
        global lvl_start
        global lvl_end
        experience = users[f'{user.id}']['experience']
        lvl_start = users[f'{user.id}']['level']
        lvl_end = int(experience ** (1/4))
        if lvl_start < lvl_end:
            users[f'{user.id}']['level'] = lvl_end
            await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}!')

    @commands.command()
    async def level(self, ctx):
            await ctx.send(f'Your level is `{lvl_end}` and your experience is `{experience}`.')
            print(f"Log/levelcmd.py: {ctx.message.author} has executed the command: level")

    @commands.command()
    async def readjson(self, ctx):
        await ctx.send(f'`{levels_json}`')

def setup(bot):
    bot.add_cog(level(bot))
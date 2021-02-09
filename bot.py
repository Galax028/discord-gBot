# pylint: disable=import-error, no-name-in-module

import os

import discord
from discord.ext import commands
from gServerTools import criticallog, errorlog, infolog, successlog

from lib.conf_importer import prebuild, token, version


class gBot(commands.Bot):
    def __init__(self, prefix : str, help_cmd, bot_token : str):
        super().__init__(command_prefix=prefix, help_command=help_cmd, case_insensitive=True)
        self.token = bot_token

    def setup(self):
        for filename in os.listdir('Python\\discord-gBot\\cogs'):
            if filename.endswith('.py'):
                try:
                    bot.load_extension(f'cogs.{filename[:-3]}')
                    successlog(f"[PRIORITY]bot.py: Cog {filename} is now loaded.")
                except Exception as e:
                    criticallog(f"[PRIORITY]bot.py: A critical error occurred while loading cog {filename}.")
                    criticallog(f"{e.__class__.__name__}: {e}")
    
    def run(self):
        infolog("[PRIORITY]bot.py: Loading cogs...")
        self.setup()
        infolog("[PRIORITY]bot.py: gBot is starting up...")
        super().run(self.token)
        successlog("[PRIORITY]bot.py: Connected to bot account.")


if __name__ == "__main__":
    os.system("")
    bot = gBot(prefix='/', help_cmd=None ,bot_token=token)
    bot.run()

from discord.ext import commands
from decouple import config
import os

bot = commands.Bot("c.", case_insensitive=True)

def load_cogs(bot):
    bot.load_extension("manager")
    for file in os.listdir('commands'):
        if file.endswith('.py'):
            cog = file[:-3]
            bot.load_extension(f'commands.{cog}')


load_cogs(bot)
TOKEN = config("TOKEN_BOT")
bot.run(TOKEN)

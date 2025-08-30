from discord.ext import commands


class Ping(commands.Cog):
    """Work with ping"""


    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Mostra o ping da API')
    async def ping(self, ctx):
        await ctx.channel.send(f'Pong! {round(self.bot.latency * 1000)}ms')



async def setup(bot):
    await bot.add_cog(Ping(bot))
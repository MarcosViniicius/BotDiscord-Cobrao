from discord.ext import commands


class Clear(commands.Cog):
    """Work with clear chat"""


    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='clear', help='Limpa o chat (requer argumento de quantidade)')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        try:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'{amount} mensagens foram excluidas desse canal de texto.')
        except:
            await ctx.message.send('Você não tem permissão para utilizar esse comando.')

def setup(bot):
    bot.add_cog(Clear(bot))
from discord.ext import commands


class Calcular(commands.Cog):
    """Work with matematic"""


    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='calcular', help='Calcula uma expressão matemática (requer argumento)')
    async def calculate_expression(self, ctx, *expression):
        expression = "".join(expression)

        response = eval(expression)
        await ctx.channel.send('A resposta é: ' + str(response))

async def setup(bot):
    await bot.add_cog(Calcular(bot))
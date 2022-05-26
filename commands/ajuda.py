from discord.ext import commands
import discord

class Ajuda(commands.Cog):
    """Work with help"""


    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ajuda', help='comando de ajuda.') 
    async def send_help(self, ctx):
        try:
            name = ctx.author.mention
            response = f'Comandos enviados no seu privado. {name}'
            mensagem_priv = (f'**Lista de comandos**\nc.help\n{prefix}sorteio [sorteios disponíveis: lol, valorant]\n{prefix}vavaarmas\nprefixo\nulto?')
            await ctx.send(response)
            await ctx.author.send(mensagem_priv)

        except discord.errors.Forbidden:
            await ctx.send('Não consigo te enviar os comandos na sua DM, habilite receber mensagens de qualquer pessoa do servidor (Opções > Privacidade)')
prefix = ("c.")
def setup(bot):
    bot.add_cog(Ajuda(bot))
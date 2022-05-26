from discord.ext import commands
import random

class Manager(commands.Cog):
    """Manage the bot"""


    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot {self.bot.user} logado com sucesso!')
        print(f"ID do bot: {self.bot.user.id}")
        channel = self.bot.get_channel(579794454244884514)
        await channel.send('OOOOOPPPPPPPAAAAAAAAAAAA FUI INICIADOOOOOOOOOOOOO')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention} Você não tem permissões suficientes para utilizar este comando.')
            await ctx.message.delete()

        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'{ctx.author.mention} Este comando não existe em minha aplicação.')
            await ctx.message.delete()
        else: 
            raise error

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "prefixo" in message.content.lower():
            await message.channel.send(f'Meu prefixo é **{prefix}**')

        if "ovo" in message.content.lower():
            await message.channel.send('PASSA A MÃO NO OVÃO DO COBRÃO VAI 🖐🥚')

        if "ulto?" in message.content.lower():
            sorteio = random.choice(['Sim', 'Não', 'será?', 'Você que escolhe!'])
            await message.channel.send(sorteio)

        await self.bot.process_commands(message)
prefix = ("c.")

def setup(bot):
    bot.add_cog(Manager(bot))
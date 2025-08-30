import discord
from discord.ext import commands

class Ajuda(commands.Cog):
    """Comando de ajuda modernizado"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ajuda', help='Mostra todos os comandos disponíveis') 
    async def send_help(self, ctx):
        try:
            embed = discord.Embed(
                title="🤖 Cobrão - Comandos Disponíveis",
                description="Aqui estão todos os comandos que posso executar:",
                color=0x00ff00
            )
            
            embed.add_field(
                name="📋 Comandos Básicos",
                value="`c.ajuda` - Mostra esta mensagem\n`c.ping` - Verifica latência\n`c.status` - Status do bot",
                inline=False
            )
            
            embed.add_field(
                name="🎲 Entretenimento", 
                value="`c.sorteio` - Sorteia algo\n`c.calcular` - Calculadora básica\n`c.surpresa` - Resposta aleatória do Cobrão",
                inline=False
            )
            
            embed.add_field(
                name="🧠 IA (Inteligência Artificial)",
                value="**Mencione o bot** (@Cobrão) + sua mensagem para conversar!\n`c.reset` - Limpa contexto de conversa",
                inline=False
            )
            
            embed.add_field(
                name="🎯 Configurações",
                value="`c.aleatorio` - Configura respostas automáticas\n`c.clear` - Limpa mensagens do chat",
                inline=False
            )
            
            embed.add_field(
                name="💬 Recursos Automáticos",
                value="• Digite 'prefixo', 'ovo' ou 'ulto?' para respostas especiais!\n• **Novo!** Cobrão responde aleatoriamente nas conversas! 🎲",
                inline=False
            )
            
            embed.set_footer(text="Use c.[comando] para executar | Exemplo: c.ping")
            
            await ctx.send(embed=embed)

        except discord.errors.Forbidden:
            fallback_msg = (
                "**🤖 Comandos do Cobrão:**\n"
                "• `c.ajuda` - Ajuda\n• `c.ping` - Latência\n• `c.status` - Status\n"
                "• `c.sorteio` - Sortear\n• `c.calcular` - Calcular\n• `c.clear` - Limpar chat\n"
                "• **Mencione-me** para conversar com IA!\n• `c.reset` - Resetar conversa"
            )
            await ctx.send(fallback_msg)

async def setup(bot):
    await bot.add_cog(Ajuda(bot))
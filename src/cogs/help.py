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
                value="`c.sorteio` - Sorteia algo\n`c.calcular` - Calculadora básica\n`c.8ball` - Bola 8 mágica\n`c.moeda` - Joga moeda\n`c.dado` - Rola dado\n`c.ppt` - Pedra, papel, tesoura\n`c.piada` - Conta piada\n`c.meme` - Meme aleatório",
                inline=False
            )

            embed.add_field(
                name="🧠 IA (Inteligência Artificial)",
                value="**Mencione o bot** (@Cobrão) + sua mensagem para conversar!\n`c.reset` - Limpa contexto de conversa\n`c.imagem` - Gera imagem com IA",
                inline=False
            )

            embed.add_field(
                name="📊 Utilitários",
                value="`c.serverinfo` - Info do servidor\n`c.userinfo` - Info de usuário\n`c.avatar` - Avatar de usuário\n`c.tempo` - Previsão do tempo\n`c.traduzir` - Traduz texto\n`c.hora` - Data e hora\n`c.escolher` - Escolha aleatória\n`c.contador` - Conta texto\n`c.listarsites` - Lista sites hospedados",
                inline=False
            )

            embed.add_field(
                name="🌐 Sites via IA",
                value="`c.criarsite` - Gera um site moderno e seguro\n`c.excluirsite` - Exclui site gerado\n`c.listarsites` - Lista todos os sites hospedados",
                inline=False
            )

            embed.add_field(
                name="🛡️ Moderação",
                value="`c.clear` - Limpa mensagens\n`c.warn` - Avisa usuário\n`c.kick` - Expulsa usuário\n`c.ban` - Bane usuário\n`c.unban` - Remove ban\n`c.mute` - Silencia usuário\n`c.unmute` - Remove silêncio",
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
                "• `c.8ball` - Bola 8\n• `c.moeda` - Jogar moeda\n• `c.dado` - Rolar dado\n"
                "• `c.ppt` - Pedra, papel, tesoura\n• `c.piada` - Piadas\n• `c.meme` - Memes\n"
                "• **Mencione-me** para conversar com IA!\n• `c.reset` - Resetar conversa\n"
                "• `c.imagem` - Gerar imagem\n• `c.serverinfo` - Info servidor\n"
                "• `c.userinfo` - Info usuário\n• `c.tempo` - Previsão tempo"
            )
            await ctx.send(fallback_msg)

async def setup(bot):
    print("🔧 Carregando Ajuda...")
    await bot.add_cog(Ajuda(bot))
    print("✅ Ajuda carregado com sucesso!")
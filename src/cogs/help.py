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
                value="""`c.ajuda` - Mostra esta mensagem
`c.ping` - Verifica latência
`c.status` - Status do bot""",
                inline=False
            )

            embed.add_field(
                name="🎲 Entretenimento",
                value="""`c.sorteio` - Sorteia algo
`c.calcular` - Calculadora básica
`c.8ball` - Bola 8 mágica
`c.moeda` - Joga moeda
`c.dado` - Rola dado
`c.ppt` - Pedra, papel, tesoura
`c.piada` - Conta piada
`c.meme` - Meme aleatório""",
                inline=False
            )

            embed.add_field(
                name="🎵 Música",
                value="""`c.join` - Entra no canal de voz
`c.leave` - Sai do canal de voz
`c.play` - Toca uma música
`c.pause` - Pausa a música
`c.resume` - Continua a música
`c.stop` - Para a música e limpa a fila
`c.skip` - Pula para a próxima música
`c.queue` - Mostra a fila de músicas
`c.np` - Mostra a música atual""",
                inline=False
            )

            embed.add_field(
                name="🧠 IA (Inteligência Artificial)",
                value="""**Mencione o bot** (@Cobrão) + sua mensagem para conversar!
`c.reset` - Limpa contexto de conversa
`c.imagem` - Gera imagem com IA""",
                inline=False
            )

            embed.add_field(
                name="✨ IA Avançada (Novo!)",
                value="""`c.historia` - Crie uma história interativa
`c.adivinhar` - Jogue adivinhação com a IA
`c.resumir` - Resume o chat do canal
`c.analisar` - Analisa o comportamento de um usuário""",
                inline=False
            )

            embed.add_field(
                name="📊 Utilitários",
                value="""`c.serverinfo` - Info do servidor
`c.userinfo` - Info de usuário
`c.avatar` - Avatar de usuário
`c.tempo` - Previsão do tempo
`c.traduzir` - Traduz texto
`c.hora` - Data e hora
`c.escolher` - Escolha aleatória
`c.contador` - Conta texto
`c.listarsites` - Lista sites hospedados""",
                inline=False
            )

            embed.add_field(
                name="🌐 Sites via IA",
                value="""`c.criarsite` - Gera um site moderno e seguro
`c.excluirsite` - Exclui site gerado
`c.listarsites` - Lista todos os sites hospedados""",
                inline=False
            )

            embed.add_field(
                name="🛡️ Moderação",
                value="""`c.clear` - Limpa mensagens
`c.warn` - Avisa usuário
`c.kick` - Expulsa usuário
`c.ban` - Bane usuário
`c.unban` - Remove ban
`c.mute` - Silencia usuário
`c.unmute` - Remove silêncio
`c.automod` - Gerencia a moderação automática""",
                inline=False
            )

            embed.add_field(
                name="💬 Recursos Automáticos",
                value="""• Digite 'prefixo', 'ovo' ou 'ulto?' para respostas especiais!
• **Novo!** Cobrão responde aleatoriamente nas conversas! 🎲""",
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

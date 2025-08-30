"""
Comandos utilitários do bot
"""
import discord
from discord.ext import commands
import random
import datetime
import aiohttp
from config.settings import EMBED_COLORS

class UtilityCommands(commands.Cog):
    """Comandos utilitários e ferramentas"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Verifica a latência do bot"""
        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latência: **{latency}ms**",
            color=EMBED_COLORS['success'] if latency < 100 else EMBED_COLORS['warning']
        )

        if latency < 50:
            embed.add_field(name="Status", value="🟢 Excelente", inline=True)
        elif latency < 100:
            embed.add_field(name="Status", value="🟡 Bom", inline=True)
        elif latency < 200:
            embed.add_field(name="Status", value="🟠 Regular", inline=True)
        else:
            embed.add_field(name="Status", value="🔴 Lento", inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int = 5):
        """Limpa mensagens do chat"""
        if amount < 1 or amount > 100:
            embed = discord.Embed(
                title="❌ Quantidade Inválida",
                description="Digite um número entre 1 e 100",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        try:
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 para incluir o comando

            embed = discord.Embed(
                title="🧹 Chat Limpo",
                description=f"**{len(deleted)-1}** mensagens removidas",
                color=EMBED_COLORS['success']
            )

            msg = await ctx.send(embed=embed)
            await msg.delete(delay=3)  # Auto-deletar após 3 segundos

        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Sem Permissão",
                description="Não tenho permissão para deletar mensagens",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)

    @commands.command(name='calcular', aliases=['calc', 'math'])
    async def calculate(self, ctx, *, expression: str):
        """Calculadora básica"""
        try:
            # Limpar a expressão (segurança básica)
            safe_expression = expression.replace(' ', '')
            allowed_chars = '0123456789+-*/().'

            if not all(c in allowed_chars for c in safe_expression):
                raise ValueError("Caracteres inválidos")

            result = eval(safe_expression)

            embed = discord.Embed(
                title="🧮 Calculadora",
                color=EMBED_COLORS['info']
            )
            embed.add_field(name="Expressão", value=f"`{expression}`", inline=False)
            embed.add_field(name="Resultado", value=f"**{result}**", inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro de Cálculo",
                description="Expressão inválida. Use apenas números e operadores básicos (+, -, *, /, ())",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)

    @commands.command(name='8ball', aliases=['bola8', 'pergunta'])
    async def eight_ball(self, ctx, *, question: str = None):
        """Faça uma pergunta e receba uma resposta mística!"""
        if not question:
            embed = discord.Embed(
                title="❓ Bola 8 Mágica",
                description="Faça uma pergunta para a bola 8!\n\nExemplo: `c.8ball Vou ganhar na loteria?`",
                color=EMBED_COLORS['info']
            )
            await ctx.send(embed=embed)
            return

        responses = [
            "✅ Sim, definitivamente!",
            "❌ Não, de jeito nenhum!",
            "🤔 Talvez...",
            "🔮 As estrelas dizem que sim",
            "🌑 As estrelas dizem que não",
            "🎲 As chances são boas",
            "⚠️ Cuidado, pode ser perigoso",
            "✨ Sim, no futuro próximo",
            "🚫 Não, melhor não",
            "💫 As respostas estão nebulosas",
            "🎯 Certamente!",
            "❓ Pergunte novamente mais tarde",
            "🌟 Os sinais apontam para sim",
            "🚧 Melhor não contar agora",
            "🎪 Definitivamente sim!",
            "🛑 Pare e pense melhor"
        ]

        response = random.choice(responses)

        embed = discord.Embed(
            title="🔮 Bola 8 Mágica",
            color=EMBED_COLORS['info']
        )
        embed.add_field(name="❓ Sua pergunta:", value=question, inline=False)
        embed.add_field(name="🎱 Resposta:", value=response, inline=False)
        embed.set_footer(text="A bola 8 nunca erra! Ou erra? 🤔")

        await ctx.send(embed=embed)

    @commands.command(name='moeda', aliases=['coin', 'flip'])
    async def coin_flip(self, ctx):
        """Joga uma moeda para cima"""
        result = random.choice(['cara', 'coroa'])
        emoji = "🪙" if result == 'cara' else "👑"

        embed = discord.Embed(
            title="🪙 Jogo da Moeda",
            description=f"A moeda caiu em... **{result.upper()}**! {emoji}",
            color=EMBED_COLORS['success'] if result == 'cara' else EMBED_COLORS['info']
        )

        await ctx.send(embed=embed)

    @commands.command(name='dado', aliases=['dice', 'roll'])
    async def roll_dice(self, ctx, sides: int = 6):
        """Rola um dado com o número de lados especificado"""
        if sides < 2 or sides > 100:
            embed = discord.Embed(
                title="❌ Número Inválido",
                description="O dado deve ter entre 2 e 100 lados",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        result = random.randint(1, sides)

        embed = discord.Embed(
            title="🎲 Rolagem de Dado",
            description=f"Dado de **{sides}** lados\nResultado: **{result}**",
            color=EMBED_COLORS['success']
        )

        # Adicionar emoji baseado no resultado
        if sides == 6:
            dice_emojis = ["", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
            embed.description += f" {dice_emojis[result]}"

        await ctx.send(embed=embed)

    @commands.command(name='ppt', aliases=['rps', 'pedrapapeltesoura'])
    async def rock_paper_scissors(self, ctx, choice: str = None):
        """Jogue pedra, papel ou tesoura contra o bot"""
        if not choice:
            embed = discord.Embed(
                title="✂️ Pedra, Papel ou Tesoura",
                description="Escolha sua jogada!\n\n`c.ppt pedra` | `c.ppt papel` | `c.ppt tesoura`",
                color=EMBED_COLORS['info']
            )
            await ctx.send(embed=embed)
            return

        choices = {
            'pedra': ['🪨', 'pedra'],
            'papel': ['📄', 'papel'],
            'tesoura': ['✂️', 'tesoura']
        }

        user_choice = choice.lower()
        if user_choice not in choices:
            embed = discord.Embed(
                title="❌ Escolha Inválida",
                description="Escolha entre: pedra, papel ou tesoura",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        bot_choice = random.choice(list(choices.keys()))

        # Determinar vencedor
        if user_choice == bot_choice:
            result = "🤝 Empate!"
            color = EMBED_COLORS['warning']
        elif (user_choice == 'pedra' and bot_choice == 'tesoura') or \
             (user_choice == 'papel' and bot_choice == 'pedra') or \
             (user_choice == 'tesoura' and bot_choice == 'papel'):
            result = "🎉 Você ganhou!"
            color = EMBED_COLORS['success']
        else:
            result = "😢 Você perdeu!"
            color = EMBED_COLORS['error']

        embed = discord.Embed(
            title="✂️ Pedra, Papel ou Tesoura",
            description=f"{result}",
            color=color
        )
        embed.add_field(
            name="🤖 Cobrão",
            value=f"{choices[bot_choice][0]} {choices[bot_choice][1].title()}",
            inline=True
        )
        embed.add_field(
            name=f"{ctx.author.display_name}",
            value=f"{choices[user_choice][0]} {choices[user_choice][1].title()}",
            inline=True
        )

        await ctx.send(embed=embed)

    @commands.command(name='serverinfo', aliases=['server', 'servidor'])
    async def server_info(self, ctx):
        """Mostra informações do servidor"""
        guild = ctx.guild

        embed = discord.Embed(
            title=f"🏠 {guild.name}",
            color=EMBED_COLORS['info']
        )

        # Informações básicas
        embed.add_field(name="👑 Dono", value=guild.owner.mention, inline=True)
        embed.add_field(name="🌍 Região", value=str(guild.region).title(), inline=True)
        embed.add_field(name="📅 Criado em", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)

        # Estatísticas
        embed.add_field(name="👥 Membros", value=guild.member_count, inline=True)
        embed.add_field(name="💬 Canais de Texto", value=len(guild.text_channels), inline=True)
        embed.add_field(name="🔊 Canais de Voz", value=len(guild.voice_channels), inline=True)

        # Status dos membros
        online = sum(1 for m in guild.members if m.status == discord.Status.online)
        idle = sum(1 for m in guild.members if m.status == discord.Status.idle)
        dnd = sum(1 for m in guild.members if m.status == discord.Status.dnd)
        offline = sum(1 for m in guild.members if m.status == discord.Status.offline)

        embed.add_field(
            name="🟢 Status dos Membros",
            value=f"Online: {online}\nAusente: {idle}\nOcupado: {dnd}\nOffline: {offline}",
            inline=False
        )

        # Ícone do servidor
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.set_footer(text=f"ID: {guild.id}")

        await ctx.send(embed=embed)

    @commands.command(name='userinfo', aliases=['user', 'usuario'])
    async def user_info(self, ctx, member: discord.Member = None):
        """Mostra informações de um usuário"""
        member = member or ctx.author

        embed = discord.Embed(
            title=f"👤 {member.display_name}",
            color=member.color if member.color != discord.Color.default() else EMBED_COLORS['info']
        )

        # Informações básicas
        embed.add_field(name="📛 Nome", value=member.name, inline=True)
        embed.add_field(name="🏷️ Apelido", value=member.nick or "Nenhum", inline=True)
        embed.add_field(name="🤖 Bot", value="✅ Sim" if member.bot else "❌ Não", inline=True)

        # Status e atividade
        status_emojis = {
            discord.Status.online: "🟢",
            discord.Status.idle: "🟡",
            discord.Status.dnd: "🔴",
            discord.Status.offline: "⚫"
        }
        embed.add_field(
            name="📊 Status",
            value=f"{status_emojis.get(member.status, '❓')} {member.status.value.title()}",
            inline=True
        )

        # Cargos
        roles = [role.mention for role in member.roles[1:]]  # Exclui @everyone
        embed.add_field(
            name="🎭 Cargos",
            value=", ".join(roles) if roles else "Nenhum cargo especial",
            inline=False
        )

        # Datas
        embed.add_field(name="📅 Entrou no servidor", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=True)
        embed.add_field(name="📅 Conta criada", value=member.created_at.strftime("%d/%m/%Y"), inline=True)

        # Avatar
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        embed.set_footer(text=f"ID: {member.id}")

        await ctx.send(embed=embed)

    @commands.command(name='avatar', aliases=['foto', 'pfp'])
    async def get_avatar(self, ctx, member: discord.Member = None):
        """Mostra o avatar de um usuário"""
        member = member or ctx.author

        embed = discord.Embed(
            title=f"🖼️ Avatar de {member.display_name}",
            color=EMBED_COLORS['info']
        )

        if member.avatar:
            embed.set_image(url=member.avatar.url)
            embed.add_field(
                name="🔗 Links",
                value=f"[PNG]({member.avatar.url}) | [JPG]({member.avatar.url}?format=jpg) | [WEBP]({member.avatar.url}?format=webp)",
                inline=False
            )
        else:
            embed.description = "Este usuário não tem um avatar personalizado."

        await ctx.send(embed=embed)

    @commands.command(name='piada', aliases=['joke', 'humor'])
    async def tell_joke(self, ctx):
        """Conta uma piada aleatória"""
        jokes = [
            "Por que o computador foi ao médico?\nPorque estava com vírus! 🦠",
            "O que o pato disse para a pata?\nVem quá! 🦆",
            "Por que o livro de matemática estava triste?\nPorque tinha muitos problemas! 📚",
            "O que é um pontinho preto no avião?\nUma aeromosca! ✈️",
            "Por que a girafa tem o pescoço comprido?\nPorque a cabeça fica longe do corpo! 🦒",
            "O que o zero disse para o oito?\nBelo cinto! 0️⃣",
            "Por que o tomate ficou vermelho?\nPorque viu a salada se vestindo! 🍅",
            "O que é que fala e tem dente mas não come?\nO pente! 🪜",
            "Por que o elefante não usa computador?\nPorque tem medo do mouse! 🐘",
            "O que o cavalo foi fazer no shopping?\nComprar ferraduras! 🐎"
        ]

        joke = random.choice(jokes)

        embed = discord.Embed(
            title="😂 Piada do Dia",
            description=joke,
            color=EMBED_COLORS['success']
        )

        await ctx.send(embed=embed)

    @commands.command(name='tempo', aliases=['weather', 'clima'])
    async def weather(self, ctx, *, city: str = None):
        """Mostra o tempo de uma cidade (usando API gratuita)"""
        if not city:
            embed = discord.Embed(
                title="🌤️ Previsão do Tempo",
                description="Digite o nome de uma cidade!\n\nExemplo: `c.tempo São Paulo`",
                color=EMBED_COLORS['info']
            )
            await ctx.send(embed=embed)
            return

        try:
            # Usando API gratuita do wttr.in
            url = f"https://wttr.in/{city}?format=%C+%t+%w+%h"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        weather_data = await response.text()

                        embed = discord.Embed(
                            title=f"🌤️ Tempo em {city.title()}",
                            description=f"```{weather_data}```",
                            color=EMBED_COLORS['info']
                        )
                        embed.set_footer(text="Dados fornecidos por wttr.in")

                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="❌ Cidade Não Encontrada",
                            description=f"Não foi possível encontrar informações para '{city}'",
                            color=EMBED_COLORS['error']
                        )
                        await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro na Consulta",
                description="Não foi possível consultar o tempo no momento.",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)

    @commands.command(name='traduzir', aliases=['translate', 'trad'])
    async def translate_text(self, ctx, lang: str = None, *, text: str = None):
        """Traduz texto para outro idioma"""
        if not lang or not text:
            embed = discord.Embed(
                title="🌐 Tradutor",
                description="Use: `c.traduzir <idioma> <texto>`\n\n**Idiomas suportados:**\n• `en` - Inglês\n• `es` - Espanhol\n• `fr` - Francês\n• `de` - Alemão\n• `it` - Italiano\n• `pt` - Português\n\nExemplo: `c.traduzir en Olá, como vai?`",
                color=EMBED_COLORS['info']
            )
            await ctx.send(embed=embed)
            return

        # Mapeamento simples de idiomas
        languages = {
            'en': 'inglês',
            'es': 'espanhol',
            'fr': 'francês',
            'de': 'alemão',
            'it': 'italiano',
            'pt': 'português'
        }

        if lang not in languages:
            embed = discord.Embed(
                title="❌ Idioma Não Suportado",
                description=f"Idioma '{lang}' não é suportado.\nUse um dos idiomas listados em `c.traduzir`",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        # Traduções simples (básicas)
        translations = {
            'en': {
                'olá': 'hello', 'como vai': 'how are you', 'obrigado': 'thank you',
                'sim': 'yes', 'não': 'no', 'bom dia': 'good morning',
                'boa noite': 'good night', 'tchau': 'bye'
            },
            'es': {
                'olá': 'hola', 'como vai': 'cómo estás', 'obrigado': 'gracias',
                'sim': 'sí', 'não': 'no', 'bom dia': 'buenos días',
                'boa noite': 'buenas noches', 'tchau': 'adiós'
            },
            'fr': {
                'olá': 'salut', 'como vai': 'comment ça va', 'obrigado': 'merci',
                'sim': 'oui', 'não': 'non', 'bom dia': 'bonjour',
                'boa noite': 'bonne nuit', 'tchau': 'au revoir'
            }
        }

        # Tradução básica
        translated_text = text
        if lang in translations:
            for pt_word, translated_word in translations[lang].items():
                translated_text = translated_text.replace(pt_word, translated_word)

        embed = discord.Embed(
            title="🌐 Tradução",
            color=EMBED_COLORS['success']
        )
        embed.add_field(name="🇧🇷 Original", value=text, inline=False)
        embed.add_field(name=f"🇺🇸 {languages[lang].title()}", value=translated_text, inline=False)
        embed.set_footer(text="Tradução básica - Para traduções avançadas, considere usar serviços especializados")

        await ctx.send(embed=embed)

    @commands.command(name='meme', aliases=['memes'])
    async def random_meme(self, ctx):
        """Mostra um meme aleatório"""
        memes = [
            "https://i.imgur.com/4M34hi2.jpg",  # Meme do Drake
            "https://i.imgur.com/t4HWQDD.jpg",  # Meme do Expanding Brain
            "https://i.imgur.com/Q1qpU9V.jpg",  # Meme do Distracted Boyfriend
            "https://i.imgur.com/9LsyOYM.jpg",  # Meme do This is Fine
            "https://i.imgur.com/8FKyO6I.jpg",  # Meme do Woman Yelling at Cat
            "https://i.imgur.com/7VzK4lI.jpg",  # Meme do Mocking SpongeBob
            "https://i.imgur.com/3V5Kj.jpg",    # Meme do Pepe Silvia
            "https://i.imgur.com/9GQHL8.jpg",   # Meme do Arthur Fist
        ]

        meme_url = random.choice(memes)

        embed = discord.Embed(
            title="😂 Meme Aleatório",
            color=EMBED_COLORS['success']
        )
        embed.set_image(url=meme_url)
        embed.set_footer(text="Fonte: Imgur | Memes clássicos da internet")

        await ctx.send(embed=embed)

    @commands.command(name='hora', aliases=['time', 'data'])
    async def current_time(self, ctx):
        """Mostra a data e hora atual"""
        now = datetime.datetime.now()

        embed = discord.Embed(
            title="🕐 Data e Hora Atual",
            color=EMBED_COLORS['info']
        )

        embed.add_field(name="📅 Data", value=now.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="🕐 Hora", value=now.strftime("%H:%M:%S"), inline=True)
        embed.add_field(name="📊 Dia da Semana", value=now.strftime("%A"), inline=True)

        # Fuso horário
        embed.add_field(
            name="🌍 Fuso Horário",
            value="UTC-3 (Brasília)",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name='escolher', aliases=['choose', 'decidir'])
    async def choose_random(self, ctx, *, options: str = None):
        """Escolhe aleatoriamente entre opções separadas por vírgula"""
        if not options:
            embed = discord.Embed(
                title="🎲 Escolha Aleatória",
                description="Separe as opções por vírgula!\n\nExemplo: `c.escolher pizza, hambúrguer, salada`",
                color=EMBED_COLORS['info']
            )
            await ctx.send(embed=embed)
            return

        # Separar opções
        choices = [opt.strip() for opt in options.split(',') if opt.strip()]

        if len(choices) < 2:
            embed = discord.Embed(
                title="❌ Poucas Opções",
                description="Forneça pelo menos 2 opções separadas por vírgula",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        chosen = random.choice(choices)

        embed = discord.Embed(
            title="🎯 Escolha Aleatória",
            description=f"Dentre as opções: **{', '.join(choices)}**\n\n**A escolhida foi:** 🎉 **{chosen}** 🎉",
            color=EMBED_COLORS['success']
        )

        await ctx.send(embed=embed)

    @commands.command(name='contador', aliases=['count', 'contar'])
    async def word_count(self, ctx, *, text: str = None):
        """Conta palavras, caracteres e linhas de um texto"""
        if not text:
            embed = discord.Embed(
                title="📊 Contador de Texto",
                description="Envie um texto para contar!\n\nExemplo: `c.contador Olá, como vai você?`",
                color=EMBED_COLORS['info']
            )
            await ctx.send(embed=embed)
            return

        # Estatísticas
        words = len(text.split())
        characters = len(text)
        characters_no_spaces = len(text.replace(' ', ''))
        lines = len(text.split('\n'))

        embed = discord.Embed(
            title="📊 Análise do Texto",
            description=f"```{text[:200]}{'...' if len(text) > 200 else ''}```",
            color=EMBED_COLORS['info']
        )

        embed.add_field(name="📝 Palavras", value=words, inline=True)
        embed.add_field(name="🔤 Caracteres", value=characters, inline=True)
        embed.add_field(name="📏 Sem espaços", value=characters_no_spaces, inline=True)
        embed.add_field(name="📄 Linhas", value=lines, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='warn', aliases=['aviso', 'advertir'])
    @commands.has_permissions(kick_members=True)
    async def warn_user(self, ctx, member: discord.Member = None, *, reason: str = "Não especificado"):
        """Avisa um usuário (requer permissão de kick)"""
        if not member:
            embed = discord.Embed(
                title="❌ Usuário Não Encontrado",
                description="Mencione um usuário para avisar!\n\nExemplo: `c.warn @usuario Spam no chat`",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Ação Inválida",
                description="Você não pode se avisar!",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                title="❌ Permissão Insuficiente",
                description="Você não pode avisar alguém com cargo igual ou superior ao seu!",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="⚠️ Usuário Avisado",
            description=f"{member.mention} foi avisado!",
            color=EMBED_COLORS['warning']
        )
        embed.add_field(name="👤 Usuário", value=member.mention, inline=True)
        embed.add_field(name="👮 Moderador", value=ctx.author.mention, inline=True)
        embed.add_field(name="📝 Motivo", value=reason, inline=False)
        embed.set_footer(text=f"ID: {member.id}")

        await ctx.send(embed=embed)

        # Tentar enviar DM para o usuário
        try:
            dm_embed = discord.Embed(
                title="⚠️ Você foi avisado!",
                description=f"Você recebeu um aviso no servidor **{ctx.guild.name}**",
                color=EMBED_COLORS['warning']
            )
            dm_embed.add_field(name="👮 Moderador", value=ctx.author.name, inline=True)
            dm_embed.add_field(name="📝 Motivo", value=reason, inline=False)
            dm_embed.set_footer(text="Comporte-se melhor da próxima vez!")

            await member.send(embed=dm_embed)
        except:
            pass  # Usuário pode ter DMs desabilitados

    @commands.command(name='kick', aliases=['expulsar'])
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, ctx, member: discord.Member = None, *, reason: str = "Não especificado"):
        """Expulsa um usuário do servidor (requer permissão de kick)"""
        if not member:
            embed = discord.Embed(
                title="❌ Usuário Não Encontrado",
                description="Mencione um usuário para expulsar!\n\nExemplo: `c.kick @usuario Spam excessivo`",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Ação Inválida",
                description="Você não pode se expulsar!",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                title="❌ Permissão Insuficiente",
                description="Você não pode expulsar alguém com cargo igual ou superior ao seu!",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        try:
            # Tentar enviar DM antes de kick
            try:
                dm_embed = discord.Embed(
                    title="🚪 Você foi expulso!",
                    description=f"Você foi expulso do servidor **{ctx.guild.name}**",
                    color=EMBED_COLORS['error']
                )
                dm_embed.add_field(name="👮 Moderador", value=ctx.author.name, inline=True)
                dm_embed.add_field(name="📝 Motivo", value=reason, inline=False)

                await member.send(embed=dm_embed)
            except:
                pass

            await member.kick(reason=reason)

            embed = discord.Embed(
                title="🚪 Usuário Expulso",
                description=f"{member.mention} foi expulso do servidor!",
                color=EMBED_COLORS['success']
            )
            embed.add_field(name="👤 Usuário", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="👮 Moderador", value=ctx.author.mention, inline=True)
            embed.add_field(name="📝 Motivo", value=reason, inline=False)

            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Sem Permissão",
                description="Não tenho permissão para expulsar este usuário.",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)

    @commands.command(name='ban', aliases=['banir'])
    @commands.has_permissions(ban_members=True)
    async def ban_user(self, ctx, member: discord.Member = None, *, reason: str = "Não especificado"):
        """Bane um usuário do servidor (requer permissão de ban)"""
        if not member:
            embed = discord.Embed(
                title="❌ Usuário Não Encontrado",
                description="Mencione um usuário para banir!\n\nExemplo: `c.ban @usuario Violação das regras`",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Ação Inválida",
                description="Você não pode se banir!",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                title="❌ Permissão Insuficiente",
                description="Você não pode banir alguém com cargo igual ou superior ao seu!",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        try:
            # Tentar enviar DM antes de ban
            try:
                dm_embed = discord.Embed(
                    title="🚫 Você foi banido!",
                    description=f"Você foi banido do servidor **{ctx.guild.name}**",
                    color=EMBED_COLORS['error']
                )
                dm_embed.add_field(name="👮 Moderador", value=ctx.author.name, inline=True)
                dm_embed.add_field(name="📝 Motivo", value=reason, inline=False)
                dm_embed.set_footer(text="Este ban é permanente!")

                await member.send(embed=dm_embed)
            except:
                pass

            await member.ban(reason=reason, delete_message_days=1)

            embed = discord.Embed(
                title="🚫 Usuário Banido",
                description=f"{member.mention} foi banido do servidor!",
                color=EMBED_COLORS['success']
            )
            embed.add_field(name="👤 Usuário", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="👮 Moderador", value=ctx.author.mention, inline=True)
            embed.add_field(name="📝 Motivo", value=reason, inline=False)

            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Sem Permissão",
                description="Não tenho permissão para banir este usuário.",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)

    @commands.command(name='unban', aliases=['desbanir'])
    @commands.has_permissions(ban_members=True)
    async def unban_user(self, ctx, *, user_id: str = None):
        """Remove o ban de um usuário (requer permissão de ban)"""
        if not user_id:
            embed = discord.Embed(
                title="❌ ID Necessário",
                description="Forneça o ID do usuário para desbanir!\n\nExemplo: `c.unban 123456789012345678`",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        try:
            user_id = int(user_id)
            user = await self.bot.fetch_user(user_id)

            try:
                await ctx.guild.unban(user)

                embed = discord.Embed(
                    title="✅ Usuário Desbanido",
                    description=f"{user.name}#{user.discriminator} foi desbanido!",
                    color=EMBED_COLORS['success']
                )
                embed.add_field(name="👤 Usuário", value=f"{user.name}#{user.discriminator}", inline=True)
                embed.add_field(name="👮 Moderador", value=ctx.author.mention, inline=True)

                await ctx.send(embed=embed)

            except discord.NotFound:
                embed = discord.Embed(
                    title="❌ Usuário Não Banido",
                    description="Este usuário não está banido neste servidor.",
                    color=EMBED_COLORS['error']
                )
                await ctx.send(embed=embed)

        except ValueError:
            embed = discord.Embed(
                title="❌ ID Inválido",
                description="Forneça um ID numérico válido!",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
        except discord.NotFound:
            embed = discord.Embed(
                title="❌ Usuário Não Encontrado",
                description="Usuário com este ID não existe.",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)

    @commands.command(name='mute', aliases=['silenciar'])
    @commands.has_permissions(moderate_members=True)
    async def mute_user(self, ctx, member: discord.Member = None, duration: str = None, *, reason: str = "Não especificado"):
        """Silencia um usuário temporariamente (requer permissão de moderar membros)"""
        if not member:
            embed = discord.Embed(
                title="❌ Usuário Não Encontrado",
                description="Mencione um usuário para silenciar!\n\nExemplo: `c.mute @usuario 1h Spam`",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Ação Inválida",
                description="Você não pode se silenciar!",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                title="❌ Permissão Insuficiente",
                description="Você não pode silenciar alguém com cargo igual ou superior ao seu!",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        # Parse duration
        if not duration:
            duration_seconds = 3600  # 1 hora por padrão
        else:
            try:
                # Parse duration (ex: 1h, 30m, 2d)
                import re
                match = re.match(r'^(\d+)([smhd])$', duration.lower())
                if match:
                    value, unit = match.groups()
                    value = int(value)
                    if unit == 's':
                        duration_seconds = value
                    elif unit == 'm':
                        duration_seconds = value * 60
                    elif unit == 'h':
                        duration_seconds = value * 3600
                    elif unit == 'd':
                        duration_seconds = value * 86400
                    else:
                        duration_seconds = 3600
                else:
                    duration_seconds = 3600
            except:
                duration_seconds = 3600

        try:
            await member.timeout(datetime.timedelta(seconds=duration_seconds), reason=reason)

            embed = discord.Embed(
                title="🔇 Usuário Silenciado",
                description=f"{member.mention} foi silenciado!",
                color=EMBED_COLORS['success']
            )
            embed.add_field(name="👤 Usuário", value=member.mention, inline=True)
            embed.add_field(name="⏱️ Duração", value=f"{duration_seconds//3600}h {(duration_seconds%3600)//60}m", inline=True)
            embed.add_field(name="👮 Moderador", value=ctx.author.mention, inline=True)
            embed.add_field(name="📝 Motivo", value=reason, inline=False)

            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Sem Permissão",
                description="Não tenho permissão para silenciar este usuário.",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)

    @commands.command(name='unmute', aliases=['desilenciar'])
    @commands.has_permissions(moderate_members=True)
    async def unmute_user(self, ctx, member: discord.Member = None, *, reason: str = "Não especificado"):
        """Remove o silêncio de um usuário (requer permissão de moderar membros)"""
        if not member:
            embed = discord.Embed(
                title="❌ Usuário Não Encontrado",
                description="Mencione um usuário para desilenciar!\n\nExemplo: `c.unmute @usuario Comportamento melhorado`",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return

        try:
            await member.timeout(None, reason=reason)

            embed = discord.Embed(
                title="🔊 Usuário Desilenciado",
                description=f"{member.mention} teve o silêncio removido!",
                color=EMBED_COLORS['success']
            )
            embed.add_field(name="👤 Usuário", value=member.mention, inline=True)
            embed.add_field(name="👮 Moderador", value=ctx.author.mention, inline=True)
            embed.add_field(name="📝 Motivo", value=reason, inline=False)

            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Sem Permissão",
                description="Não tenho permissão para desilenciar este usuário.",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)

async def setup(bot):
    print("🔧 Carregando UtilityCommands...")
    await bot.add_cog(UtilityCommands(bot))
    print("✅ UtilityCommands carregado com sucesso!")
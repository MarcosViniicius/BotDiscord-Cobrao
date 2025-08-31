"""
Cog de Entretenimento com IA
"""
import discord
from discord.ext import commands
from openai import OpenAI
from config.settings import OPENAI_API_KEY, EMBED_COLORS, OPENAI_MODEL
from src.utils.helpers import send_temp_message

class EntertainmentAI(commands.Cog):
    """Comandos de entretenimento que usam IA."""

    def __init__(self, bot):
        self.bot = bot
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        # Armazena as histórias ativas por canal: { channel_id: [messages] }
        self.active_stories = {}
        # Armazena os jogos de adivinhação: { channel_id: { "secret": "palavra", "messages": [] } }
        self.active_guesses = {}

    @commands.command(name='historia', help='Cria uma história interativa com IA. Use c.historia fim para terminar.')
    async def historia(self, ctx, *, action: str = None):
        """Inicia ou continua uma história interativa.
        
        Se não houver história, uma nova começa.
        Se houver, sua ação continua a narrativa.
        Use 'c.historia fim' para encerrar a história atual.
        """
        channel_id = ctx.channel.id

        # Subcomando para terminar a história
        if action and action.lower() == 'fim':
            if channel_id in self.active_stories:
                del self.active_stories[channel_id]
                embed = discord.Embed(
                    title="📖 Fim da História",
                    description="A aventura neste canal foi concluída. Comece uma nova com `c.historia`!",
                    color=EMBED_COLORS['info']
                )
                await ctx.send(embed=embed)
            else:
                await send_temp_message(ctx, "Não há nenhuma história em andamento neste canal.", 10)
            return

        async with ctx.typing():
            # Iniciar uma nova história
            if channel_id not in self.active_stories:
                system_prompt = (
                    "Você é um Mestre de RPG para Discord. Sua tarefa é criar e narrar uma história de aventura interativa. "
                    "Comece com uma introdução intrigante em um cenário de fantasia, terror ou ficção científica. "
                    "Apresente uma situação e termine sempre com a pergunta: 'O que você faz agora?'. "
                    "Mantenha as respostas com no máximo 2 parágrafos."
                )
                
                messages = [{"role": "system", "content": system_prompt}]
                
                try:
                    response = self.openai_client.chat.completions.create(
                        model=OPENAI_MODEL,
                        messages=messages,
                        max_tokens=300
                    )
                    story_part = response.choices[0].message.content

                    # Salvar o contexto
                    messages.append({"role": "assistant", "content": story_part})
                    self.active_stories[channel_id] = messages

                    embed = discord.Embed(
                        title="📖 Uma Nova Aventura Começa!",
                        description=story_part,
                        color=EMBED_COLORS['success']
                    )
                    embed.set_footer(text="Responda com 'c.historia [sua ação]' ou 'c.historia fim' para terminar.")
                    await ctx.send(embed=embed)

                except Exception as e:
                    await ctx.send(f"❌ Erro ao contatar a IA: {e}")
                return

            # Continuar uma história existente
            if not action:
                await send_temp_message(ctx, "Uma história já está em andamento. Diga o que você quer fazer com `c.historia [sua ação]`.", 10)
                return

            messages = self.active_stories[channel_id]
            messages.append({"role": "user", "content": action})

            try:
                response = self.openai_client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=messages,
                    max_tokens=300
                )
                story_part = response.choices[0].message.content

                # Atualizar o contexto
                messages.append({"role": "assistant", "content": story_part})
                self.active_stories[channel_id] = messages

                embed = discord.Embed(
                    title="⚔️ A Aventura Continua...",
                    description=story_part,
                    color=EMBED_COLORS['info']
                )
                embed.set_footer(text="Responda com 'c.historia [sua ação]' ou 'c.historia fim' para terminar.")
                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"❌ Erro ao contatar a IA: {e}")

    @commands.group(name='adivinhar', help='Jogue um jogo de adivinhação com a IA.', invoke_without_command=True)
    async def adivinhar(self, ctx, *, question: str = None):
        channel_id = ctx.channel.id

        if ctx.invoked_subcommand is None:
            # Se não há jogo ativo, começa um novo
            if channel_id not in self.active_guesses:
                async with ctx.typing():
                    system_prompt = (
                        "Você é um mestre do jogo de adivinhação. Pense em um objeto, animal ou personagem famoso. "
                        "Guarde este segredo. Responda às perguntas do usuário apenas com 'Sim', 'Não', 'Quase', 'Talvez', 'Irrelevante' ou 'Pode ser'. "
                        "Primeiro, diga ao usuário que você pensou em algo e peça a primeira pergunta."
                    )
                    
                    # Gerar um segredo aleatório
                    secret_response = self.openai_client.chat.completions.create(
                        model=OPENAI_MODEL,
                        messages=[{"role": "system", "content": "Gere uma única palavra ou nome de personagem/animal para um jogo de adivinhação. Ex: 'elefante', 'Napoleão Bonaparte', 'vassoura'."}],
                        max_tokens=20
                    )
                    secret_word = secret_response.choices[0].message.content.strip().replace('.', '')

                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "system", "content": f"O segredo que você pensou é: '{secret_word}'. Lembre-se disso e não revele."}
                    ]
                    
                    # Mensagem inicial da IA
                    initial_response = self.openai_client.chat.completions.create(
                        model=OPENAI_MODEL,
                        messages=messages,
                        max_tokens=50
                    )
                    initial_message = initial_response.choices[0].message.content

                    messages.append({"role": "assistant", "content": initial_message})
                    self.active_guesses[channel_id] = {"secret": secret_word, "messages": messages}

                    embed = discord.Embed(
                        title="🤔 Jogo da Adivinhação",
                        description=initial_message,
                        color=EMBED_COLORS['info']
                    )
                    embed.set_footer(text="Use 'c.adivinhar [pergunta]', 'c.adivinhar chutar [palpite]' ou 'c.adivinhar fim'.")
                    await ctx.send(embed=embed)
                return
            
            # Se há um jogo ativo, processa a pergunta
            if not question:
                await send_temp_message(ctx, "Um jogo já está em andamento. Faça uma pergunta ou use `c.adivinhar chutar [palpite]`.", 10)
                return

            async with ctx.typing():
                game = self.active_guesses[channel_id]
                game["messages"].append({"role": "user", "content": question})

                response = self.openai_client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=game["messages"],
                    max_tokens=20
                )
                answer = response.choices[0].message.content

                game["messages"].append({"role": "assistant", "content": answer})
                self.active_guesses[channel_id] = game

                await ctx.send(f"**Sua pergunta:** `{question}`\n**Resposta da IA:** `{answer}`")

    @adivinhar.command(name='chutar')
    async def adivinhar_chutar(self, ctx, *, guess: str):
        channel_id = ctx.channel.id
        if channel_id not in self.active_guesses:
            await send_temp_message(ctx, "Nenhum jogo de adivinhação ativo. Comece um com `c.adivinhar`.", 10)
            return

        game = self.active_guesses[channel_id]
        secret = game['secret']

        # Pergunta para a IA se o chute está correto
        verification_prompt = [
            {"role": "system", "content": f"O segredo é '{secret}'. O usuário chutou '{guess}'. A resposta está correta? Responda apenas 'sim' ou 'não'."}
        ]
        
        response = self.openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=verification_prompt,
            max_tokens=5
        )
        is_correct = response.choices[0].message.content.lower()

        if 'sim' in is_correct:
            embed = discord.Embed(
                title="🎉 Você Acertou!",
                description=f"Parabéns, a resposta era **{secret}**!",
                color=EMBED_COLORS['success']
            )
            await ctx.send(embed=embed)
            del self.active_guesses[channel_id]
        else:
            embed = discord.Embed(
                title="❌ Errado!",
                description=f"Não, a resposta não é `{guess}`. Tente novamente!",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)

    @adivinhar.command(name='fim')
    async def adivinhar_fim(self, ctx):
        channel_id = ctx.channel.id
        if channel_id in self.active_guesses:
            secret = self.active_guesses[channel_id]['secret']
            embed = discord.Embed(
                title="🤔 Fim de Jogo",
                description=f"O jogo terminou. A resposta era **{secret}**.",
                color=EMBED_COLORS['info']
            )
            await ctx.send(embed=embed)
            del self.active_guesses[channel_id]
        else:
            await send_temp_message(ctx, "Nenhum jogo de adivinhação ativo para terminar.", 10)


async def setup(bot):
    await bot.add_cog(EntertainmentAI(bot))

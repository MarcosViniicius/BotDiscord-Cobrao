
Cog de Administração com IA
"""
import discord
from discord.ext import commands
from openai import OpenAI
from config.settings import OPENAI_API_KEY, EMBED_COLORS, OPENAI_MODEL
from src.utils.helpers import send_temp_message
import datetime

class AdminAI(commands.Cog):
    """Comandos de administração que usam IA."""

    def __init__(self, bot):
        self.bot = bot
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.automod_config = {
            "enabled": False,
            "log_channel": None,
            "ignored_channels": []
        }

    @commands.command(name='resumir', help='Resume as últimas mensagens de um canal.')
    @commands.has_permissions(manage_messages=True)
    async def resumir(self, ctx, limit: int = 50):
        """Resume as últimas [limit] mensagens do canal (padrão: 50)."""
        if limit > 200 or limit < 10:
            await send_temp_message(ctx, "Por favor, escolha um limite entre 10 e 200 mensagens.", 10)
            return

        embed = discord.Embed(
            title="📝 Resumindo Conversa...",
            description=f"Analisando as últimas {limit} mensagens deste canal. Isso pode levar um momento...",
            color=EMBED_COLORS['info']
        )
        msg = await ctx.send(embed=embed)

        try:
            messages = []
            async for message in ctx.channel.history(limit=limit):
                if not message.author.bot:
                    messages.append(f"{message.author.name}: {message.content}")
            
            messages.reverse()
            conversation = "\n".join(messages)

            if not conversation.strip():
                await msg.edit(embed=discord.Embed(title="📝 Resumo da Conversa", description="Não há mensagens de usuários para resumir.", color=EMBED_COLORS['info']))
                return

            system_prompt = """Você é um assistente de moderação para Discord. Sua tarefa é ler a transcrição de um chat e resumir os pontos principais. Seja conciso e objetivo. Destaque os tópicos discutidos, perguntas importantes, decisões tomadas e o sentimento geral da conversa (positivo, negativo, neutro)."""

            response = self.openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": conversation}
                ],
                max_tokens=400
            )
            summary = response.choices[0].message.content

            summary_embed = discord.Embed(
                title=f"📝 Resumo das Últimas {limit} Mensagens",
                description=summary,
                color=EMBED_COLORS['success']
            )
            await msg.edit(embed=summary_embed)

        except discord.Forbidden:
            await msg.edit(embed=discord.Embed(title="❌ Erro de Permissão", description="Não tenho permissão para ler o histórico deste canal.", color=EMBED_COLORS['error']))
        except Exception as e:
            await msg.edit(embed=discord.Embed(title="❌ Erro", description=f"Ocorreu um erro ao gerar o resumo: {e}", color=EMBED_COLORS['error']))

    @commands.command(name='analisar', help='Analisa o comportamento recente de um usuário.')
    @commands.has_permissions(moderate_members=True)
    async def analisar(self, ctx, member: discord.Member, limit: int = 100):
        """Analisa as últimas [limit] mensagens de um usuário no servidor."""
        if limit > 200 or limit < 10:
            await send_temp_message(ctx, "Por favor, escolha um limite entre 10 e 200 mensagens.", 10)
            return

        embed = discord.Embed(
            title=f"🔍 Analisando {member.display_name}...",
            description=f"Coletando as últimas {limit} mensagens do usuário em todo o servidor. Isso pode demorar...",
            color=EMBED_COLORS['info']
        )
        msg = await ctx.send(embed=embed)

        try:
            user_messages = []
            for channel in ctx.guild.text_channels:
                if channel.permissions_for(ctx.me).read_message_history:
                    async for message in channel.history(limit=limit * 2):
                        if message.author == member:
                            user_messages.append(f"[{message.channel.name}] {message.content}")
                            if len(user_messages) >= limit:
                                break
                if len(user_messages) >= limit:
                    break
            
            if not user_messages:
                await msg.edit(embed=discord.Embed(title=f"🔍 Análise de {member.display_name}", description="Não encontrei mensagens recentes deste usuário nos canais que consigo ler.", color=EMBED_COLORS['info']))
                return

            conversation = "\n".join(user_messages)

            system_prompt = """Você é um assistente de moderação do Discord. Sua tarefa é analisar uma coleção de mensagens de um único usuário e fornecer um relatório de comportamento. O relatório deve ser neutro e baseado apenas nos dados fornecidos. Inclua os seguintes pontos em formato de tópicos (use markdown):
- **Sentimento Geral:** (Positivo, Neutro, Negativo, Misto)
- **Tópicos Comuns:** (Liste os principais assuntos abordados pelo usuário)
- **Potenciais Infrações:** (Sinalize qualquer linguagem que pareça ser spam, ofensiva, tóxica ou que possa quebrar regras comuns de um servidor. Se nada for encontrado, declare 'Nenhuma infração óbvia encontrada.')
- **Conclusão:** (Um breve resumo de uma linha sobre o perfil de comunicação do usuário)."""

            response = self.openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": conversation}
                ],
                max_tokens=500
            )
            analysis = response.choices[0].message.content

            analysis_embed = discord.Embed(
                title=f"🔍 Análise de Comportamento: {member.display_name}",
                description=analysis,
                color=EMBED_COLORS['success']
            )
            analysis_embed.set_footer(text=f"Análise baseada em {len(user_messages)} mensagens.")
            await msg.edit(embed=analysis_embed)

        except discord.Forbidden:
            await msg.edit(embed=discord.Embed(title="❌ Erro de Permissão", description="Não tenho permissões para ler o histórico de mensagens em canais suficientes.", color=EMBED_COLORS['error']))
        except Exception as e:
            await msg.edit(embed=discord.Embed(title="❌ Erro", description=f"Ocorreu um erro ao gerar a análise: {e}", color=EMBED_COLORS['error']))

    @commands.group(name='automod', help='Gerencia o sistema de moderação automática com IA.')
    @commands.has_permissions(administrator=True)
    async def automod(self, ctx):
        if ctx.invoked_subcommand is None:
            status = "Ativado" if self.automod_config["enabled"] else "Desativado"
            log_channel = f"<#{self.automod_config['log_channel']}>" if self.automod_config["log_channel"] else "Nenhum"
            embed = discord.Embed(title="AutoMod IA Status", color=EMBED_COLORS['info'])
            embed.add_field(name="Status", value=status)
            embed.add_field(name="Canal de Logs", value=log_channel)
            await ctx.send(embed=embed)

    @automod.command(name='toggle')
    async def automod_toggle(self, ctx):
        self.automod_config["enabled"] = not self.automod_config["enabled"]
        status = "Ativado" if self.automod_config["enabled"] else "Desativado"
        await ctx.send(f"✅ AutoMod IA foi **{status}**.")

    @automod.command(name='logchannel')
    async def automod_logchannel(self, ctx, channel: discord.TextChannel):
        self.automod_config["log_channel"] = channel.id
        await ctx.send(f"✅ Canal de logs do AutoMod definido para {channel.mention}.")

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if not self.automod_config["enabled"] or message.author.bot or not message.guild:
    #         return
        
    #     if message.channel.id in self.automod_config["ignored_channels"] or message.author.guild_permissions.administrator:
    #         return

    #     content = message.content
    #     system_prompt = """Você é um sistema de moderação para Discord. Analise a seguinte mensagem e classifique-a em uma das categorias: 'OK', 'SPAM', 'TOXIC', 'INSULT', 'THREAT'. Responda apenas com a categoria."""

    #     try:
    #         response = self.openai_client.chat.completions.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "system", "content": system_prompt},
    #                 {"role": "user", "content": content}
    #             ],
    #             max_tokens=10
    #         )
    #         category = response.choices[0].message.content.strip().upper()

    #         if category != 'OK':
    #             log_channel_id = self.automod_config["log_channel"]
    #             if log_channel_id:
    #                 log_channel = self.bot.get_channel(log_channel_id)
    #                 if log_channel:
    #                     embed = discord.Embed(title="🚨 Alerta do AutoMod IA 🚨", color=EMBED_COLORS['error'])
    #                     embed.add_field(name="Usuário", value=message.author.mention, inline=False)
    #                     embed.add_field(name="Mensagem", value=content, inline=False)
    #                     embed.add_field(name="Categoria", value=category, inline=False)
    #                     embed.add_field(name="Canal", value=message.channel.mention, inline=False)
    #                     await log_channel.send(embed=embed)
                
    #             await message.delete()
    #             await send_temp_message(message.channel, f"{message.author.mention}, sua mensagem foi removida por violar as regras ({category}).", 15)

    #     except Exception as e:
    #         print(f"[AutoMod Error] {e}")

async def setup(bot):
    await bot.add_cog(AdminAI(bot))
"""
Cog principal do bot - Gerenciamento e IA
"""
import discord
from discord.ext import commands
import random
import datetime
from openai import OpenAI
from config.settings import *
from src.utils.helpers import RandomResponseManager, ContextManager

class CoreManager(commands.Cog):
    @commands.command(name='imagem', aliases=['img', 'gerarimagem'])
    async def gerar_imagem(self, ctx, *, prompt: str = None):
        """Gera uma imagem criativa usando IA (DALL-E). Exemplo: c.imagem um dragão azul voando sobre uma cidade futurista"""
        if not prompt or len(prompt.strip()) < 5:
            await ctx.send("❌ Forneça uma descrição detalhada para gerar a imagem. Exemplo: `c.imagem um dragão azul voando sobre uma cidade futurista`")
            return

        # Controle de duplicidade por usuário e canal
        if not hasattr(self.bot, '_imagem_prompts'):
            self.bot._imagem_prompts = {}
        user_id = ctx.author.id
        canal_id = ctx.channel.id
        prompt_key = (user_id, canal_id, prompt.strip().lower())

        if prompt_key in self.bot._imagem_prompts:
            await ctx.send("⚠️ Você já gerou uma imagem com este prompt recentemente neste canal. Tente outro prompt ou aguarde.")
            return
        self.bot._imagem_prompts[prompt_key] = True

        # Limpar prompts antigos para evitar memory leak
        if len(self.bot._imagem_prompts) > 100:
            # Remove entradas antigas (mantém apenas as 50 mais recentes)
            keys_to_remove = list(self.bot._imagem_prompts.keys())[:-50]
            for key in keys_to_remove:
                del self.bot._imagem_prompts[key]

        embed = discord.Embed(
            title="🖼️ Gerando imagem...",
            description=f"Prompt: `{prompt[:200]}`\n\nDica: Seja criativo e evite termos de marcas ou jogos!",
            color=EMBED_COLORS['info']
        )
        msg = await ctx.send(embed=embed)

        try:
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
            embed = discord.Embed(
                title="✅ Imagem Gerada!",
                description=f"Prompt: `{prompt[:200]}`",
                color=EMBED_COLORS['success']
            )
            embed.set_image(url=image_url)
            embed.set_footer(text="Powered by DALL-E | Use c.imagem para criar mais!")
            await msg.edit(embed=embed)
        except Exception as e:
            await msg.edit(content=f"❌ Erro ao gerar imagem: {e}\nDica: Evite termos de marcas, jogos ou conteúdo sensível.")
        # Limpa duplicidade após 3 minutos
        async def limpar_prompt():
            await discord.utils.sleep_until(discord.utils.utcnow() + datetime.timedelta(minutes=3))
            if prompt_key in self.bot._imagem_prompts:
                del self.bot._imagem_prompts[prompt_key]
        self.bot.loop.create_task(limpar_prompt())
    """Gerenciamento principal do bot e funcionalidades de IA"""

    def __init__(self, bot):
        self.bot = bot
        
        # Cliente OpenAI
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Gerenciadores
        self.random_manager = RandomResponseManager()
        self.context_manager = ContextManager(MAX_CONTEXT_MESSAGES)
        
        # Configurações
        self.random_response_chance = DEFAULT_RANDOM_CHANCE
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Evento executado quando o bot fica online"""
        print(f'🤖 Bot {self.bot.user} logado com sucesso!')
        print(f'📊 ID: {self.bot.user.id}')
        print(f'🌐 Servidores: {len(self.bot.guilds)}')

        # Definir status
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, 
                name=BOT_ACTIVITY
            )
        )
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Tratamento de erros de comandos"""
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ Permissão Negada",
                description=f"{ctx.author.mention} Você não tem permissões para usar este comando.",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed, delete_after=5)

        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="❓ Comando Não Encontrado", 
                description=f"{ctx.author.mention} Use `c.ajuda` para ver comandos disponíveis.",
                color=EMBED_COLORS['warning']
            )
            await ctx.send(embed=embed, delete_after=5)
        else: 
            raise error

    @commands.command(name='status')
    async def status_command(self, ctx):
        """Mostra informações do bot"""
        embed = discord.Embed(
            title="🤖 Status do Bot Cobrão", 
            color=EMBED_COLORS['info']
        )
        embed.add_field(name="🌐 Servidores", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="👥 Usuários", value=len(self.bot.users), inline=True)
        embed.add_field(name="📡 Latência", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="🎲 Respostas Aleatórias", value=f"{self.random_response_chance*100}%", inline=True)
        embed.add_field(name="🧠 Contextos Ativos", value=len(self.context_manager.conversations), inline=True)
        embed.add_field(name="🎯 Modelo IA", value=OPENAI_MODEL, inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name='reset')
    async def reset_context(self, ctx):
        """Reseta o contexto de conversa do canal atual"""
        success = self.context_manager.clear_context(ctx.channel.id)
        
        if success:
            embed = discord.Embed(
                title="🧠 Contexto Resetado",
                description="Memória de conversa limpa com sucesso!",
                color=EMBED_COLORS['success']
            )
        else:
            embed = discord.Embed(
                title="ℹ️ Nenhum Contexto",
                description="Não havia contexto para limpar neste canal.",
                color=EMBED_COLORS['info']
            )
        
        await ctx.send(embed=embed)

    @commands.command(name='aleatorio')
    async def configure_random(self, ctx, chance: float = None):
        """Configura a chance de respostas aleatórias (0.0 a 1.0)"""
        if chance is None:
            current = self.random_response_chance * 100
            embed = discord.Embed(
                title="🎲 Configuração Atual",
                description=f"Chance de respostas aleatórias: **{current}%**\n\nUse `c.aleatorio 0.1` para definir 10%",
                color=EMBED_COLORS['info']
            )
            await ctx.send(embed=embed)
            return
            
        if chance < 0 or chance > 1:
            embed = discord.Embed(
                title="❌ Valor Inválido",
                description="A chance deve ser entre 0.0 (0%) e 1.0 (100%)",
                color=EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
            
        self.random_response_chance = chance
        embed = discord.Embed(
            title="✅ Configuração Atualizada",
            description=f"Chance de respostas aleatórias: **{chance*100}%**",
            color=EMBED_COLORS['success']
        )
        await ctx.send(embed=embed)

    # Removido: comando de teste básico (não utilizado)

    @commands.command(name='debug')
    @commands.is_owner()
    async def debug_command(self, ctx):
        """Comando de debug para o owner"""
        embed = discord.Embed(
            title="🔧 Debug do Bot",
            color=EMBED_COLORS['info']
        )
        
        # Informações do servidor
        embed.add_field(
            name="🌐 Servidor Atual",
            value=f"**{ctx.guild.name}**\nID: {ctx.guild.id}\nMembros: {ctx.guild.member_count}",
            inline=False
        )
        
        # Permissões
        perms = ctx.channel.permissions_for(ctx.me)
        embed.add_field(
            name="🔐 Permissões",
            value=f"Ler mensagens: {'✅' if perms.read_messages else '❌'}\nEnviar mensagens: {'✅' if perms.send_messages else '❌'}\nEmbed links: {'✅' if perms.embed_links else '❌'}",
            inline=True
        )
        
        # Configurações
        embed.add_field(
            name="⚙️ Configurações",
            value=f"Prefixo: `{COMMAND_PREFIX}`\nChance aleatória: {self.random_response_chance*100}%",
            inline=True
        )
        
        await ctx.send(embed=embed)

    # Removido: comando de resposta aleatória forçada (não utilizado)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignora mensagens do próprio bot
        if message.author.bot:
            return

        # Responde com IA quando o bot for mencionado
        if self.bot.user in message.mentions:
            await self._handle_ai_response(message)

        # Permite que outros comandos funcionem normalmente
        await self.bot.process_commands(message)

    async def _handle_special_responses(self, message):
        """Processa respostas especiais (palavras-chave)"""
        content = message.content.lower()
        if "prefixo" in content:
            await message.channel.send(f'Meu prefixo é **{COMMAND_PREFIX}**')
        elif "ovo" in content:
            await message.channel.send('PASSA A MÃO NO OVÃO DO COBRÃO VAI 🖐🥚')
        elif "ulto?" in content:
            response = random.choice(['Sim', 'Não', 'será?', 'Você que escolhe!'])
            await message.channel.send(response)

    async def _handle_ai_response(self, message):
        """Processa resposta com IA (ChatGPT)"""
        channel_id = message.channel.id
        user_message = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
        if not user_message:
            user_message = "Olá! Como posso ajudar?"

        # Controle de duplicidade para respostas IA
        if not hasattr(self.bot, '_ai_responses'):
            self.bot._ai_responses = {}
        ai_key = (channel_id, user_message.strip().lower()[:100])  # Limitar tamanho da chave

        if ai_key in self.bot._ai_responses:
            print(f"🤖 Resposta IA duplicada detectada, ignorando: {user_message[:50]}...")
            return
        self.bot._ai_responses[ai_key] = True

        # Limpar respostas antigas
        if len(self.bot._ai_responses) > 200:
            keys_to_remove = list(self.bot._ai_responses.keys())[:-100]
            for key in keys_to_remove:
                del self.bot._ai_responses[key]

        try:
            context = self.context_manager.get_context(channel_id)
            messages = [
                {"role": "system", "content": "Você é o Cobrão, um assistente divertido e útil para Discord. Seja amigável, mas mantenha o humor do 'cobrão'."}
            ]
            messages.extend(context)
            messages.append({"role": "user", "content": user_message})
            response = self.openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=MAX_TOKENS
            )
            reply = response.choices[0].message.content
            self.context_manager.add_message(channel_id, "user", user_message)
            self.context_manager.add_message(channel_id, "assistant", reply)
            await message.channel.send(reply)

            # Limpar duplicidade após 5 minutos
            async def limpar_ai_response():
                await discord.utils.sleep_until(discord.utils.utcnow() + datetime.timedelta(minutes=5))
                if ai_key in self.bot._ai_responses:
                    del self.bot._ai_responses[ai_key]
            self.bot.loop.create_task(limpar_ai_response())

        except Exception as e:
            print(f"❌ Erro OpenAI: {e}")
            await message.channel.send("🤖 Ops! Estou com problemas técnicos. Tente novamente em alguns instantes!")

    async def _handle_random_response(self, message):
        """Processa resposta aleatória"""
        self.random_manager.update_last_message_time(message.channel.id)
        action = random.choice(['message', 'react', 'react', 'react'])
        if action == 'message':
            response = self.random_manager.get_random_response()
            await message.channel.send(response)
        else:
            emoji = self.random_manager.get_reaction_emoji()
            try:
                await message.add_reaction(emoji)
            except:
                pass  # Ignora se não conseguir reagir

async def setup(bot):
    print("🔧 Carregando CoreManager...")
    await bot.add_cog(CoreManager(bot))
    print("✅ CoreManager carregado com sucesso!")

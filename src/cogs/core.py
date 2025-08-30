"""
Cog principal do bot - Gerenciamento e IA
"""
import discord
from discord.ext import commands
import random
import datetime
import asyncio
from openai import OpenAI
from config.settings import *
from src.utils.helpers import RandomResponseManager, ContextManager, send_temp_message

class CoreManager(commands.Cog):
    
    def __init__(self, bot):
        print(f"🏗️ INIT: Inicializando CoreManager...")
        self.bot = bot
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.random_manager = RandomResponseManager()
        self.context_manager = ContextManager()
        self.random_response_chance = 0.05  # 5% de chance por padrão
        
        # Verificar se já existe outro CoreManager carregado
        for cog_name, cog_instance in bot.cogs.items():
            if isinstance(cog_instance, CoreManager) and cog_instance != self:
                print(f"⚠️ DUPLICADO: Já existe um CoreManager carregado!")
                raise Exception("CoreManager já existe!")
        
        print(f"✅ INIT: CoreManager inicializado com ID {id(self)}")
    
    async def send_long_message(self, channel, text):
        """Envia uma mensagem, truncando se exceder o limite do Discord"""
        print(f"📤 SEND_MSG: Enviando {len(text)} caracteres para canal {channel.id}")
        
        # Limite do Discord é 2000 caracteres, deixamos margem de segurança
        if len(text) > 1950:
            truncated_text = text[:1900] + "...\n\n*[Resposta truncada - limite do Discord]*"
            print(f"✂️ TRUNCADO: Mensagem reduzida de {len(text)} para {len(truncated_text)} caracteres")
            text = truncated_text
        
        try:
            message = await channel.send(text)
            print(f"✅ ENVIADO: Mensagem enviada (ID: {message.id})")
            return message
            
        except Exception as e:
            print(f"❌ ERRO: {e}")
            # Fallback: tenta enviar versão ainda menor
            try:
                emergency_text = text[:1500] + "...\n\n*[Erro no envio]*"
                message = await channel.send(emergency_text)
                print(f"🚑 FALLBACK: Versão emergencial enviada")
                return message
            except:
                print(f"💥 FALHA CRÍTICA: Não foi possível enviar mensagem")
                return None

    @commands.command(name='imagem', aliases=['img', 'gerarimagem'])
    async def gerar_imagem(self, ctx, *, prompt: str = None):
        """Gera uma imagem criativa usando IA (DALL-E). Exemplo: c.imagem um dragão azul voando sobre uma cidade futurista"""
        user_id = ctx.author.id
        
        # Controle de processamento ativo por usuário
        if not hasattr(self.bot, '_processing_users'):
            self.bot._processing_users = set()
        
        # Se o usuário já tem uma requisição sendo processada, ignora
        if user_id in self.bot._processing_users:
            embed = discord.Embed(
                title="⏳ Processando...",
                description=f"{ctx.author.mention} Aguarde! Estou processando sua requisição anterior.\n\nTente novamente em alguns segundos.",
                color=EMBED_COLORS['warning']
            )
            embed.set_footer(text="Anti-flood: Uma requisição por vez")
            await send_temp_message(ctx, embed, 5)
            return
        
        # Marcar usuário como processando
        self.bot._processing_users.add(user_id)
        
        try:
            if not prompt or len(prompt.strip()) < 5:
                embed = discord.Embed(
                    title="❌ Prompt Inválido",
                    description="Forneça uma descrição detalhada para gerar a imagem.\n\nExemplo: `c.imagem um dragão azul voando sobre uma cidade futurista`",
                    color=EMBED_COLORS['error']
                )
                await send_temp_message(ctx, embed, 8)
                return

            # Controle de limite diário de imagens (20 por usuário por dia)
            if not hasattr(self.bot, '_daily_image_limit'):
                self.bot._daily_image_limit = {}
            
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            user_key = f"{user_id}_{today}"
            
            # Verificar limite diário
            current_count = self.bot._daily_image_limit.get(user_key, 0)
            if current_count >= 20:
                embed = discord.Embed(
                    title="🚫 Limite Diário Atingido",
                    description=f"{ctx.author.mention} Você atingiu o limite de **20 imagens por dia**!\n\nTente novamente amanhã.",
                    color=EMBED_COLORS['error']
                )
                embed.set_footer(text="Limite resetado à meia-noite")
                await send_temp_message(ctx, embed, 10)
                return

            # Controle de duplicidade por usuário e canal
            if not hasattr(self.bot, '_imagem_prompts'):
                self.bot._imagem_prompts = {}
            canal_id = ctx.channel.id
            prompt_key = (user_id, canal_id, prompt.strip().lower())

            if prompt_key in self.bot._imagem_prompts:
                embed = discord.Embed(
                    title="⚠️ Prompt Duplicado",
                    description=f"{ctx.author.mention} Você já gerou uma imagem com este prompt recentemente neste canal.\n\nTente outro prompt ou aguarde.",
                    color=EMBED_COLORS['warning']
                )
                await send_temp_message(ctx, embed, 8)
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

            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
            
            # Incrementar contador diário após sucesso
            self.bot._daily_image_limit[user_key] = current_count + 1
            remaining = 20 - (current_count + 1)
            
            embed = discord.Embed(
                title="✅ Imagem Gerada!",
                description=f"Prompt: `{prompt[:200]}`",
                color=EMBED_COLORS['success']
            )
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Powered by DALL-E | Restam {remaining} imagens hoje | Use c.imagem para criar mais!")
            await msg.edit(embed=embed)
            
            # Limpar dados antigos do limite diário (manter apenas últimos 2 dias)
            if len(self.bot._daily_image_limit) > 1000:
                yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                keys_to_remove = [k for k in self.bot._daily_image_limit.keys() if not k.endswith(today) and not k.endswith(yesterday)]
                for key in keys_to_remove:
                    del self.bot._daily_image_limit[key]
            
            # Limpa duplicidade após 3 minutos
            async def limpar_prompt():
                await discord.utils.sleep_until(discord.utils.utcnow() + datetime.timedelta(minutes=3))
                if prompt_key in self.bot._imagem_prompts:
                    del self.bot._imagem_prompts[prompt_key]
            self.bot.loop.create_task(limpar_prompt())
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro na Geração",
                description=f"Erro ao gerar imagem: {str(e)[:200]}\n\n💡 Dica: Evite termos de marcas, jogos ou conteúdo sensível.",
                color=EMBED_COLORS['error']
            )
            await send_temp_message(ctx, embed, 10)
            
        finally:
            # Sempre remove o usuário da lista de processamento
            self.bot._processing_users.discard(user_id)
    
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
            await send_temp_message(ctx, embed, 6)

        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="❓ Comando Não Encontrado", 
                description=f"{ctx.author.mention} Use `c.ajuda` para ver comandos disponíveis.",
                color=EMBED_COLORS['warning']
            )
            await send_temp_message(ctx, embed, 6)
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
            await send_temp_message(ctx, embed, 8)
            return
            
        self.random_response_chance = chance
        embed = discord.Embed(
            title="✅ Configuração Atualizada",
            description=f"Chance de respostas aleatórias: **{chance*100}%**",
            color=EMBED_COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='limpar_cache', hidden=True)
    @commands.is_owner()
    async def limpar_cache_antiflood(self, ctx):
        """Limpa o cache anti-duplicidade (apenas owner)"""
        # Limpar usuários em processamento
        if hasattr(self.bot, '_processing_users'):
            users_count = len(self.bot._processing_users)
            self.bot._processing_users.clear()
        else:
            users_count = 0
        
        # Limpar mensagens processadas
        if hasattr(self.bot, '_processed_messages'):
            messages_count = len(self.bot._processed_messages)
            self.bot._processed_messages.clear()
        else:
            messages_count = 0
        
        # Limpar contextos de IA
        if hasattr(self.bot, '_ai_responses'):
            ai_count = len(self.bot._ai_responses)
            self.bot._ai_responses.clear()
        else:
            ai_count = 0
        
        embed = discord.Embed(
            title="🧹 Cache Limpo",
            description=f"""Cache anti-duplicidade limpo com sucesso!
            
**Estatísticas:**
• Usuários processando: {users_count}
• Mensagens processadas: {messages_count}
• Respostas IA: {ai_count}
            
Todos os caches foram resetados.""",
            color=EMBED_COLORS['success']
        )
        
        await ctx.send(embed=embed)
        print(f"🧹 CACHE: Limpo por {ctx.author.name} - {users_count + messages_count + ai_count} itens removidos")

    @commands.command(name='status_cache', hidden=True)
    @commands.is_owner()
    async def status_cache_antiflood(self, ctx):
        """Mostra o status do cache anti-duplicidade (apenas owner)"""
        # Verificar usuários em processamento
        processing_users = len(getattr(self.bot, '_processing_users', set()))
        
        # Verificar mensagens processadas
        processed_messages = len(getattr(self.bot, '_processed_messages', set()))
        
        # Verificar respostas IA
        ai_responses = len(getattr(self.bot, '_ai_responses', {}))
        
        embed = discord.Embed(
            title="📊 Status do Cache Anti-Duplicidade",
            color=EMBED_COLORS['info']
        )
        
        embed.add_field(
            name="👥 Usuários Processando",
            value=f"{processing_users} usuários",
            inline=True
        )
        
        embed.add_field(
            name="📝 Mensagens Processadas",
            value=f"{processed_messages} mensagens",
            inline=True
        )
        
        embed.add_field(
            name="🤖 Respostas IA Cache",
            value=f"{ai_responses} respostas",
            inline=True
        )
        
        # Status geral
        if processing_users == 0:
            status = "🟢 Normal"
            status_desc = "Nenhum usuário sendo processado"
        elif processing_users < 5:
            status = "🟡 Ativo"
            status_desc = f"{processing_users} usuários sendo processados"
        else:
            status = "🔴 Alto"
            status_desc = f"Muitos usuários ({processing_users}) sendo processados"
        
        embed.add_field(
            name="🔍 Status Geral",
            value=f"{status}\n{status_desc}",
            inline=False
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='testar_duplicata', hidden=True)
    @commands.is_owner()
    async def testar_duplicata(self, ctx):
        """Testa o sistema anti-duplicata (apenas owner)"""
        embed = discord.Embed(
            title="🧪 Teste de Anti-Duplicata",
            description="""Este comando testa se o sistema anti-duplicata está funcionando.
            
**Como testar:**
1. Após usar este comando, mencione o bot várias vezes rapidamente
2. O bot deve responder apenas uma vez por menção
3. Use `!status_cache` para ver estatísticas
4. Use `!limpar_cache` se necessário resetar
            
**Status Atual:**""",
            color=EMBED_COLORS['info']
        )
        
        # Status dos sistemas
        processing_count = len(getattr(self.bot, '_processing_users', set()))
        messages_count = len(getattr(self.bot, '_processed_messages', set()))
        
        embed.add_field(
            name="🔒 Sistema de Lock",
            value="✅ Ativo" if hasattr(self.bot, '_processing_users') else "❌ Inativo",
            inline=True
        )
        
        embed.add_field(
            name="🛡️ Anti-Duplicata",
            value="✅ Ativo" if hasattr(self.bot, '_processed_messages') else "❌ Inativo",
            inline=True
        )
        
        embed.add_field(
            name="📊 Usuários/Mensagens",
            value=f"{processing_count}/{messages_count}",
            inline=True
        )
        
        await ctx.send(embed=embed)

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
        
        # Estado anti-flood/duplicidade
        processing_users = len(getattr(self.bot, '_processing_users', set()))
        processed_messages = len(getattr(self.bot, '_processed_messages', set()))
        
        embed.add_field(
            name="🛡️ Anti-Flood",
            value=f"Usuários processando: {processing_users}\nMensagens processadas: {processed_messages}",
            inline=True
        )
        
        # Contextos ativos
        embed.add_field(
            name="🧠 Contextos IA",
            value=f"Conversas ativas: {len(self.context_manager.conversations)}",
            inline=True
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='limpar_estado', hidden=True)
    @commands.is_owner()
    async def clear_state(self, ctx):
        """Limpa o estado anti-duplicidade do bot (owner only)"""
        # Limpar usuários em processamento
        if hasattr(self.bot, '_processing_users'):
            processing_count = len(self.bot._processing_users)
            self.bot._processing_users.clear()
        else:
            processing_count = 0
        
        # Limpar mensagens processadas
        if hasattr(self.bot, '_processed_messages'):
            messages_count = len(self.bot._processed_messages)
            self.bot._processed_messages.clear()
        else:
            messages_count = 0
        
        embed = discord.Embed(
            title="🧹 Estado Limpo",
            description=f"Estado anti-duplicidade resetado!\n\n"
                       f"• Usuários em processamento removidos: **{processing_count}**\n"
                       f"• Mensagens processadas removidas: **{messages_count}**",
            color=EMBED_COLORS['success']
        )
        
        await ctx.send(embed=embed)
        print(f"🧹 Estado anti-duplicidade limpo por {ctx.author.name}")

    # Removido: comando de resposta aleatória forçada (não utilizado)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignora mensagens do próprio bot
        if message.author.bot:
            return

        # Responde com IA quando o bot for mencionado
        if self.bot.user in message.mentions:
            print(f"📢 MENÇÃO: {message.author.name} mencionou o bot (msg {message.id})")
            await self._handle_ai_response(message)
            return

        # Não processar comandos aqui - o bot já faz isso automaticamente
        # O listener deve apenas lidar com mensões e respostas especiais

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
        user_id = message.author.id
        message_id = message.id  # ID único da mensagem
        user_message = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
        if not user_message:
            user_message = "Olá! Como posso ajudar?"

        print(f"🔍 INICIO: Processando mensagem {message_id} de {message.author.name}")

        # Controle de processamento ativo por usuário
        if not hasattr(self.bot, '_processing_users'):
            self.bot._processing_users = set()
        
        # Se o usuário já tem uma requisição sendo processada, ignora TOTALMENTE
        if user_id in self.bot._processing_users:
            print(f"🚫 BLOQUEADO: Usuário {message.author.name} já processando (msg {message_id})")
            return
        
        # Controle de mensagens já processadas (por ID da mensagem)
        if not hasattr(self.bot, '_processed_messages'):
            self.bot._processed_messages = set()
        
        if message_id in self.bot._processed_messages:
            print(f"🚫 BLOQUEADO: Mensagem {message_id} já processada")
            return
        
        # Marcar mensagem como processada IMEDIATAMENTE
        self.bot._processed_messages.add(message_id)
        print(f"✅ MARCADO: Mensagem {message_id} marcada como processada")
        
        # Marcar usuário como processando IMEDIATAMENTE
        self.bot._processing_users.add(user_id)
        print(f"🔒 BLOQUEADO: Usuário {message.author.name} agora está processando")
        
        # Limpar mensagens processadas antigas (manter apenas últimas 1000)
        if len(self.bot._processed_messages) > 1000:
            old_messages = list(self.bot._processed_messages)[:500]
            for old_id in old_messages:
                self.bot._processed_messages.discard(old_id)
            print(f"🧹 LIMPEZA: Removidas {len(old_messages)} mensagens antigas do cache")
        
        try:
            context = self.context_manager.get_context(channel_id)
            messages = [
                {"role": "system", "content": "Você é o Cobrão, um assistente divertido e útil para Discord. Seja amigável, mas mantenha o humor do 'cobrão'. IMPORTANTE: Mantenha suas respostas concisas e dentro de 1800 caracteres no máximo, pois mensagens muito longas são truncadas. Seja direto e objetivo."}
            ]
            messages.extend(context)
            messages.append({"role": "user", "content": user_message})
            
            print(f"🤖 OPENAI: Enviando para IA - {user_message[:50]}...")
            
            response = self.openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=MAX_TOKENS
            )
            reply = response.choices[0].message.content
            
            print(f"📝 RESPOSTA: IA retornou {len(reply)} caracteres")
            
            # Salvar no contexto (sempre a resposta original completa)
            self.context_manager.add_message(channel_id, "user", user_message)
            self.context_manager.add_message(channel_id, "assistant", reply)
            
            print(f"💾 CONTEXTO: Salvo no histórico do canal {channel_id}")
            
            # Enviar resposta (dividida em partes se necessário)
            await self.send_long_message(message.channel, reply)
            
            print(f"✅ ENVIADO: Resposta enviada para {message.author.name}")

        except Exception as e:
            print(f"❌ ERRO: OpenAI falhou - {e}")
            embed = discord.Embed(
                title="🤖 Problema Técnico",
                description=f"{message.author.mention} Ops! Estou com problemas técnicos.\n\nTente novamente em alguns instantes!",
                color=EMBED_COLORS['error']
            )
            await send_temp_message(message, embed, 8)
        
        finally:
            # Sempre remove o usuário da lista de processamento
            self.bot._processing_users.discard(user_id)
            print(f"🔓 LIBERADO: {message.author.name} liberado do processamento")
            print(f"🏁 FIM: Processamento da mensagem {message_id} concluído")

async def setup(bot):
    print("🔧 Carregando CoreManager...")
    await bot.add_cog(CoreManager(bot))
    print("✅ CoreManager carregado com sucesso!")

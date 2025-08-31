"""
Bot Discord Cobrão - Assistente com IA
Arquivo principal unificado
"""
import discord
from discord.ext import commands
import asyncio
import os
import sys

# Adicionar src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

from config.logging_config import setup_logging
from config.settings import DISCORD_TOKEN, COMMAND_PREFIX

# Configurar logging otimizado
setup_logging(debug_mode=False)  # Mude para True para debug detalhado

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True  # Necessário para IA e respostas
print(f"🔧 Intents configurados: message_content={intents.message_content}")

# Criar bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, case_insensitive=True)
print(f"🤖 Bot criado com prefixo: {COMMAND_PREFIX}")

async def load_cogs():
    """Carrega todas as extensões do bot"""
    print("📦 Iniciando carregamento das cogs...")

    # Lista de cogs para carregar
    cogs_to_load = [
        'src.cogs.core',      # Gerenciamento principal e IA
        'src.cogs.help',      # Comando de ajuda
        'src.cogs.utils',     # Utilitários (ping, clear, calc)
        'src.cogs.games',     # Jogos e sorteios
        'src.cogs.sitegen',   # Geração e exclusão de sites via IA
    ]

    for cog in cogs_to_load:
        try:
            print(f"🔧 Carregando: {cog}")
            await bot.load_extension(cog)
            print(f"✅ Carregado: {cog}")
        except Exception as e:
            print(f"❌ Erro ao carregar {cog}: {e}")

    print("📦 Todas as extensões carregadas!")

async def main():
    """Função principal do bot"""
    print("🚀 Iniciando Bot Cobrão...")
    
    async with bot:
        await load_cogs()
        print("📦 Todas as extensões carregadas!")
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot finalizado pelo usuário.")
    except Exception as e:
        print(f"💥 Erro crítico: {e}")

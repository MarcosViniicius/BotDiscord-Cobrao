"""
Bot Discord Cobrão - Assistente com IA
Versão moderna e organizada
"""
import discord
from discord.ext import commands
import asyncio
import os
import sys

# Adicionar src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

from config.settings import DISCORD_TOKEN, COMMAND_PREFIX

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True  # Necessário para IA e respostas

# Criar bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, case_insensitive=True)

async def load_cogs():
    """Carrega todas as extensões do bot"""
    cogs_dir = os.path.join('src', 'cogs')
    
    # Lista de cogs para carregar
    cogs_to_load = [
        'src.cogs.core',      # Gerenciamento principal e IA
        'src.cogs.help',      # Comando de ajuda
        'src.cogs.utils',     # Utilitários (ping, clear, calc)
        'src.cogs.games',     # Jogos e sorteios
    ]
    
    for cog in cogs_to_load:
        try:
            await bot.load_extension(cog)
            print(f"✅ Carregado: {cog}")
        except Exception as e:
            print(f"❌ Erro ao carregar {cog}: {e}")

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

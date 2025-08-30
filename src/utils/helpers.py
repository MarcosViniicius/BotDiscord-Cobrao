"""
Funções utilitárias para o bot Cobrão
"""
import random
import asyncio
from config.settings import RANDOM_RESPONSES, REACTION_EMOJIS, RANDOM_COOLDOWN

class RandomResponseManager:
    """Gerencia as respostas aleatórias do bot"""
    
    def __init__(self):
        self.last_random_message = {}
    
    def get_random_response(self):
        """Retorna uma resposta aleatória"""
        return random.choice(RANDOM_RESPONSES)
    
    def get_reaction_emoji(self):
        """Retorna um emoji aleatório para reação"""
        return random.choice(REACTION_EMOJIS)
    
    def should_respond_randomly(self, message, random_chance):
        """Determina se o bot deve responder aleatoriamente"""
        channel_id = message.channel.id
        
        # Não responder se for comando
        if message.content.startswith('c.'):
            return False
            
        # Não responder se foi mencionado
        if message.guild and message.guild.me in message.mentions:
            return False
            
        # Verificar cooldown
        current_time = asyncio.get_event_loop().time()
        if channel_id in self.last_random_message:
            time_diff = current_time - self.last_random_message[channel_id]
            if time_diff < RANDOM_COOLDOWN:
                return False
        
        # Chance aleatória
        return random.random() < random_chance
    
    def update_last_message_time(self, channel_id):
        """Atualiza o tempo da última mensagem aleatória"""
        current_time = asyncio.get_event_loop().time()
        self.last_random_message[channel_id] = current_time

class ContextManager:
    """Gerencia o contexto de conversas"""
    
    def __init__(self, max_messages=10):
        self.conversations = {}
        self.max_messages = max_messages
    
    def add_message(self, channel_id, role, content):
        """Adiciona uma mensagem ao contexto"""
        if channel_id not in self.conversations:
            self.conversations[channel_id] = []
        
        self.conversations[channel_id].append({
            "role": role,
            "content": content
        })
        
        # Manter apenas as últimas mensagens
        if len(self.conversations[channel_id]) > self.max_messages:
            self.conversations[channel_id] = self.conversations[channel_id][-self.max_messages:]
    
    def get_context(self, channel_id):
        """Retorna o contexto de um canal"""
        return self.conversations.get(channel_id, [])
    
    def clear_context(self, channel_id):
        """Limpa o contexto de um canal"""
        if channel_id in self.conversations:
            del self.conversations[channel_id]
            return True
        return False

def format_time(seconds):
    """Formata tempo em segundos para uma string legível"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds/60)}m"
    else:
        return f"{int(seconds/3600)}h"

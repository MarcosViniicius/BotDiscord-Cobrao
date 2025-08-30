"""
Configurações do bot Cobrão
"""
from decouple import config

# Configurações do Discord
DISCORD_TOKEN = config('TOKEN_BOT')
COMMAND_PREFIX = 'c.'

# Configurações da OpenAI
OPENAI_API_KEY = config('OPENAI_API_KEY')
OPENAI_MODEL = 'gpt-4o'
MAX_TOKENS = 800  # Reduzido para garantir que respostas fiquem dentro do limite do Discord

# Configurações de respostas aleatórias
DEFAULT_RANDOM_CHANCE = 0.05  # 5%
RANDOM_COOLDOWN = 300  # 5 minutos
MAX_CONTEXT_MESSAGES = 10

# Configurações de status
BOT_ACTIVITY = "menções | c.ajuda"

# Lista de respostas aleatórias
RANDOM_RESPONSES = [
    "🐍 SSSSSS... alguém me chamou?",
    "Cobrão sempre atento! 👁️",
    "Interessante... 🤔",
    "Hmmm, deixa eu pensar nisso... 💭",
    "🐍 *som de cobra pensativa*",
    "Vocês sabiam que eu tenho poderes de IA? ✨",
    "Estou observando essa conversa... 👀",
    "Cobrão aprova essa discussão! 👍",
    "Alguém disse COBRÃO? Não? Ok então... 😅",
    "🎲 Momento aleatório do Cobrão!",
    "Psiu... menciona o @Cobrão se quiser conversar comigo! 😉",
    "Essa conversa tá interessante... continua! 🍿",
    "🐍 Cobrão mode: ON",
    "Vocês são muito engraçados! 😂",
    "Hmm... *analisando conversa* 🤖",
    "Alguém quer jogar alguma coisa? Uso c.sorteio! 🎯",
    "Momento filosófico: por que a cobra não tem pernas? 🤷‍♂️",
    "Tô aqui só observando mesmo... 🕵️",
    "Cobrão sempre vigilante! 🛡️",
    "Essa conversa merece um emoji: 🔥"
]

# Emojis para reações
REACTION_EMOJIS = ["🐍", "👀", "🤔", "😂", "👍", "🔥", "✨", "🎯", "💭", "😉"]

# Cores para embeds
EMBED_COLORS = {
    'success': 0x00ff00,
    'error': 0xff0000,
    'info': 0x00aaff,
    'warning': 0xffaa00
}

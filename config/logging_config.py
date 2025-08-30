"""
Configurações de logging otimizadas para o Bot Cobrão
"""
import logging

def setup_logging(debug_mode: bool = False):
    """
    Configura o sistema de logging do bot
    
    Args:
        debug_mode: Se True, habilita logs mais detalhados
    """
    # Nível de log baseado no modo
    level = logging.DEBUG if debug_mode else logging.INFO
    
    # Configuração base do logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Reduzir logs verbosos de bibliotecas externas
    external_loggers = [
        'discord.gateway',
        'discord.http', 
        'discord.voice_state',
        'discord.client',
        'websockets.client',
        'websockets.server',
        'urllib3.connectionpool'
    ]
    
    for logger_name in external_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
    
    # Configurar loggers específicos do bot
    if not debug_mode:
        # Em modo normal, reduzir logs de debug
        logging.getLogger('VoiceManager').setLevel(logging.INFO)
    
    print("📝 Sistema de logging configurado")
    print(f"🔧 Modo debug: {'Ativado' if debug_mode else 'Desativado'}")

# Configurações para diferentes ambientes
LOGGING_PRESETS = {
    'production': {
        'level': logging.WARNING,
        'format': '%(asctime)s - %(levelname)s - %(message)s'
    },
    'development': {
        'level': logging.INFO,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    },
    'debug': {
        'level': logging.DEBUG,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    }
}

def get_preset_config(preset: str = 'development'):
    """
    Retorna configuração de logging predefinida
    
    Args:
        preset: 'production', 'development' ou 'debug'
    """
    return LOGGING_PRESETS.get(preset, LOGGING_PRESETS['development'])

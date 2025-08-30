"""
Arquivo de inicialização simples - mantém compatibilidade
"""
import subprocess
import sys
import os

def main():
    """Executa o bot principal"""
    print("🐍 Iniciando Bot Cobrão...")
    
    # Verificar se está no diretório correto
    if not os.path.exists('bot.py'):
        print("❌ Erro: Execute este arquivo na raiz do projeto!")
        return
    
    # Executar o bot principal
    try:
        subprocess.run([sys.executable, 'bot.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Bot finalizado.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar: {e}")

if __name__ == "__main__":
    main()

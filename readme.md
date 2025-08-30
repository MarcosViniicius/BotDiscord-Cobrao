# 🐍 Bot Discord Cobrão

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.4.0-blue?logo=discord)](https://discordpy.readthedocs.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green?logo=openai)](https://platform.openai.com/)

> Bot Discord com IA (OpenAI), comandos inteligentes, utilitários, jogos e integração total com Docker.

---

## ✨ Funcionalidades

- **IA inteligente**: Respostas contextuais e naturais via OpenAI
- **Respostas aleatórias**: Interação divertida
- **Utilitários**: Calculadora, ping, clear, sorteio, status, debug
- **Jogos**: 8ball, dado, moeda, memes
- **Moderação**: Limpeza de mensagens, sorteios
- **Ajuda interativa**: Comando `c.ajuda` sempre atualizado

## 🚀 Instalação Rápida

1. **Clone o projeto:**

   ```bash
   git clone <seu-repositorio>
   cd BotDiscord-Cobrao
   ```

2. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o .env:**
   Crie um arquivo `.env` com:

   ```env
   TOKEN_BOT=seu_token_do_discord_aqui
   OPENAI_API_KEY=sua_chave_openai_aqui
   ```

4. **Habilite Intents no Discord:**

   - Acesse [Discord Developer Portal](https://discord.com/developers/applications/)
   - Sua App → Bot → Privileged Gateway Intents
   - Habilite **MESSAGE CONTENT INTENT**

5. **Execute o bot:**

   ```bash
   python main.py
   ```

6. **Docker (opcional):**
   ```bash
   docker compose up --build
   ```

---

## 📋 Comandos Principais

| Comando                         | Função                         |
| ------------------------------- | ------------------------------ |
| `@Cobrão <mensagem>`            | Converse com IA por texto      |
| `c.ajuda`                       | Lista todos os comandos        |
| `c.status`                      | Informações do bot             |
| `c.ping`                        | Latência do bot                |
| `c.sorteio`                     | Sorteio interativo             |
| `c.calcular <exp>`              | Calculadora                    |
| `c.clear <quantidade>`          | Limpa mensagens                |
| `c.reset`                       | Limpa contexto de conversa     |
| `c.aleatorio <0.0-1.0>`         | Configura respostas aleatórias |
| `c.debug`                       | Informações técnicas           |
| `c.meme`                        | Meme aleatório                 |
| `c.piada`                       | Piada aleatória                |
| `c.tempo <cidade>`              | Previsão do tempo              |
| `c.traduzir <idioma> <texto>`   | Traduz texto básico            |
| `c.dado [lados]`                | Rola um dado                   |
| `c.moeda`                       | Joga uma moeda                 |
| `c.8ball <pergunta>`            | Bola 8 mágica                  |
| `c.ppt <escolha>`               | Pedra, papel ou tesoura        |
| `c.avatar [@user]`              | Mostra avatar do usuário       |
| `c.userinfo [@user]`            | Info de usuário                |
| `c.serverinfo`                  | Info do servidor               |
| `c.escolher pizza, salada, ...` | Escolha aleatória              |
| `c.contador <texto>`            | Conta palavras/caracteres      |

---

## 🐳 Docker

O projeto já possui `Dockerfile` e `docker-compose.yml` prontos!

```bash
docker compose up --build
```

Você pode customizar variáveis no `.env` e montar volumes para desenvolvimento.

---

## 🛠 Tecnologias

- Python 3.11+
- Discord.py 2.4.0
- OpenAI API
- AsyncIO
- Docker

---

## 🧹 Estrutura do Projeto

- `main.py` — ponto de entrada único do bot
- `src/cogs/` — comandos organizados por temas (core, utils, games, help)
- `config/` — configurações e logging
- `.env.example` — modelo para variáveis de ambiente
- `requirements.txt` — dependências essenciais
- `Dockerfile` e `docker-compose.yml` — para uso com Docker

## 🤝 Suporte & Contribuição

- Use `c.debug` para informações técnicas
- Verifique os logs do bot
- Abra uma issue ou pull request
- Sugestões e melhorias são bem-vindas!

---

🐍 **Feito com Python** | 💙 **Discord.py** | 🤖 **Powered by OpenAI**

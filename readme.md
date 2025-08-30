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

### 1. Clonando o projeto

```bash
git clone <seu-repositorio>
cd BotDiscord-Cobrao
```

### 2. Configurando ambiente

```bash
pip install -r requirements.txt
```

### 3. Configuração do .env

Crie um arquivo `.env`:

```env
TOKEN_BOT=seu_token_do_discord_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 4. Habilite Intents no Discord

1. Acesse [Discord Developer Portal](https://discord.com/developers/applications/)
2. Sua App → Bot → Privileged Gateway Intents
3. Habilite **MESSAGE CONTENT INTENT**

### 5. Executando localmente

```bash
python main.py
```

### 6. Executando com Docker

```bash
docker compose up --build
```

---

## 📋 Comandos Principais

| Comando                 | Função                         |
| ----------------------- | ------------------------------ |
| `@Cobrão <mensagem>`    | Converse com IA por texto      |
| `c.ajuda`               | Lista todos os comandos        |
| `c.status`              | Informações do bot             |
| `c.ping`                | Latência do bot                |
| `c.sorteio`             | Sorteio interativo             |
| `c.calcular <exp>`      | Calculadora                    |
| `c.clear <quantidade>`  | Limpa mensagens                |
| `c.reset`               | Limpa contexto de conversa     |
| `c.aleatorio <0.0-1.0>` | Configura respostas aleatórias |
| `c.debug`               | Informações técnicas           |

---

## 🐳 Docker

O projeto já possui `Dockerfile` e `docker-compose.yml` prontos!

```bash
docker compose up --build
```

Você pode customizar variáveis no `.env` e montar volumes para desenvolvimento.

---

## 🛠 Tecnologias

- [Python 3.11+](https://www.python.org/)
- [Discord.py 2.4.0](https://discordpy.readthedocs.io/)
- [OpenAI API](https://platform.openai.com/)
- AsyncIO
- Docker

---

## 🤝 Suporte & Contribuição

- Use `c.debug` para informações técnicas
- Verifique os logs do bot
- Abra uma issue ou pull request
- Sugestões e melhorias são bem-vindas!

---

🐍 **Feito com Python** | 💙 **Discord.py** | 🤖 **Powered by OpenAI**

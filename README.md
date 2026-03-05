<h1 align="center">👁️ Watcher Bot</h1>
<p align="center">
  Bot Discord de monitoramento e alertas em tempo real.
</p>
<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img alt="Discord.py" src="https://img.shields.io/badge/Discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white"/>
  <img alt="Deploy" src="https://img.shields.io/badge/Deploy-Vercel-black?style=for-the-badge&logo=vercel"/>
</p>

---

## 📋 Sobre

**Watcher Bot** é um bot para **Discord** desenvolvido em Python com a biblioteca `discord.py`. Monitora eventos específicos e envia alertas personalizados para canais Discord, com suporte a comandos e configurações por servidor.

## ✨ Funcionalidades

- 👁️ Monitoramento em tempo real de eventos
- 🔔 Alertas customizados para jogadores/usuários específicos
- 💬 Comandos interativos via prefix ou slash commands
- ⚙️ Configuração por servidor Discord
- 🌐 Deploy disponível em: [watcher-bot-eight.vercel.app](https://watcher-bot-eight.vercel.app)

## 📦 Instalação

```bash
git clone https://github.com/LuigiNeto01/Watcher_bot.git
cd Watcher_bot

pip install -r requirements.txt

# Configure o token do bot:
cp .gitignore .env.example  # crie um .env
# Adicione: DISCORD_TOKEN=seu_token_aqui
```

## ⚙️ Configuração

Crie um arquivo `.env` na raiz:

```env
DISCORD_TOKEN=seu_token_bot_discord
```

## 🔧 Uso

```bash
python bot.py
```

O bot ficará online e pronto para receber comandos no seu servidor Discord.

## 🚀 Tecnologias

- **Python 3.x**
- **discord.py** — Biblioteca para bots Discord
- **python-dotenv** — Variáveis de ambiente

## 📝 Licença

Este projeto está disponível como open source.

---

<p align="center">Feito com ❤️ por <a href="https://github.com/LuigiNeto01">LuigiNeto01</a> | <a href="https://watcher-bot-eight.vercel.app">Demo</a></p>

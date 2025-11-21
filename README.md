# Watcher Bot

Bot simples de Discord que monitora os canais de voz e avisa quando alguem entra em call.

## Como usar

1. Crie um bot no [Portal do Discord](https://discord.com/developers/applications), copie o token e convide-o para seu servidor com a permissao `View Channels`.
2. Descubra o ID do canal de texto onde quer receber os alertas (clique com o botao direito -> **Copiar ID**, com o modo de desenvolvedor ativado).
3. Configure as variaveis de ambiente (ou crie um arquivo `.env` na raiz do projeto com as mesmas chaves):

   ```powershell
   setx DISCORD_TOKEN "<TOKEN_DO_BOT>"
   setx ALERT_CHANNEL_ID "<ID_NUMERICO_DO_CANAL>"
   ```

   Arquivo `.env` equivalente:

   ```
   DISCORD_TOKEN=<TOKEN_DO_BOT>
   ALERT_CHANNEL_ID=<ID_NUMERICO_DO_CANAL>
   ```

4. Instale as dependencias e execute o bot:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python bot.py
   ```

Quando um usuario (nao bot) entrar em qualquer canal de voz, o bot enviara um embed no canal configurado avisando que ha player em call e indicando qual canal foi usado.

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

Quando um usuario (nao bot) entrar em qualquer canal de voz (estava fora de call e conectou), o bot enviara um embed no canal configurado avisando que ha player em call e indicando qual canal foi usado.

## Jogadores monitorados

O arquivo `bot.py` possui a lista `WATCHED_PLAYER_HANDLES` com os nicks que devem disparar alertas. Essa lista foi preenchida com:

- `.thierry.`
- `leon3to`
- `cl4upy`
- `lucaabenda_57238`
- `luigineto`

Certifique-se de que o `display name`, `global name` ou `username` no Discord de cada amigo combina exatamente com esses identificadores (sem o `@`). Quando um deles entra em call:

- Todos os outros recebem um ping no canal configurado, exceto o proprio jogador que entrou.
- Apenas quem estiver fora da call naquele momento recebe o ping. Se dois amigos ja estao na call e um terceiro entra, so os outros que estiverem fora sao notificados.
- Certifique-se de adicionar ou remover nomes da lista `WATCHED_PLAYER_HANDLES` conforme o grupo crescer ou mudar.

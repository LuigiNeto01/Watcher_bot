import asyncio
import logging
import os
from typing import Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv

# -------------------------------------------------------------------------------------------------
# Bot configuration
# -------------------------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# Load .env file if present so the script works out of the box for local usage.
load_dotenv()

DISCORD_TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")
ALERT_CHANNEL_ID_RAW: Optional[str] = os.getenv("ALERT_CHANNEL_ID") or os.getenv(
    "ALERT_CHANNEL_ID_RAW"
)

if not DISCORD_TOKEN:
    raise RuntimeError(
        "Environment variable DISCORD_TOKEN is missing. "
        "Create a Discord bot, copy the token and export it before running."
    )

if not ALERT_CHANNEL_ID_RAW:
    raise RuntimeError(
        "Environment variable ALERT_CHANNEL_ID is missing. "
        "Set it to the numeric ID of the text channel that should receive alerts."
    )

try:
    ALERT_CHANNEL_ID = int(ALERT_CHANNEL_ID_RAW)
except ValueError as exc:
    raise RuntimeError("ALERT_CHANNEL_ID must be a numeric channel ID") from exc

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready() -> None:
    logging.info("Watcher bot conectado como %s (%s)", bot.user, bot.user.id)  # type: ignore[arg-type]


async def send_voice_alert(member: discord.Member, channel: discord.VoiceChannel) -> None:
    """Send a notification to the configured alert channel."""
    alert_channel = bot.get_channel(ALERT_CHANNEL_ID)
    if alert_channel is None:
        try:
            alert_channel = await bot.fetch_channel(ALERT_CHANNEL_ID)
        except discord.DiscordException as exc:
            logging.error(
                "Nao foi possivel buscar o canal de alertas %s: %s",
                ALERT_CHANNEL_ID,
                exc,
            )
            return

    if not isinstance(alert_channel, discord.TextChannel):
        logging.error(
            "Canal de alertas %s nao encontrado ou nao e de texto. Verifique o ID.",
            ALERT_CHANNEL_ID,
        )
        return

    embed = discord.Embed(
        title="Player em call",
        description=f"{member.mention} entrou na call {channel.mention}",
        color=discord.Color.green(),
    )
    embed.set_footer(text="Watcher Bot")

    await alert_channel.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())


@bot.event
async def on_voice_state_update(
    member: discord.Member,
    before: discord.VoiceState,
    after: discord.VoiceState,
) -> None:
    """Trigger when someone joins a voice channel."""
    if member.bot:
        return

    # Ignore cases where the channel does not change or user leaves a voice channel.
    if before.channel == after.channel or after.channel is None:
        return

    await send_voice_alert(member, after.channel)


if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except KeyboardInterrupt:
        logging.info("Encerrando watcher bot...")
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.stop()

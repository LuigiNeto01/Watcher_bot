import asyncio
import logging
import os
from typing import Dict, List, Optional, Set

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

# Players that should trigger custom alerts.
WATCHED_PLAYER_HANDLES = [
    ".thierry.",
    "leon3to",
    "cl4upy",
    "lucaabenda_57238",
    "luigineto",
]


def _normalize_handle(value: str) -> str:
    """Normalize handles/usernames for matching."""
    return value.strip().lower().lstrip("@")


WATCHED_PLAYER_KEYS: Set[str] = {_normalize_handle(name) for name in WATCHED_PLAYER_HANDLES}

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


def _identify_watch_key(member: discord.Member) -> Optional[str]:
    """Return the normalized watch key for this guild member if it is tracked."""
    for candidate in (member.global_name, member.display_name, member.name):
        if not candidate:
            continue
        normalized = _normalize_handle(candidate)
        if normalized in WATCHED_PLAYER_KEYS:
            return normalized
    return None


def _collect_watch_members(guild: discord.Guild) -> Dict[str, discord.Member]:
    """Build a mapping of watched handles to guild members."""
    mapping: Dict[str, discord.Member] = {}
    for guild_member in guild.members:
        key = _identify_watch_key(guild_member)
        if key:
            mapping[key] = guild_member
    return mapping


def _watched_handles_in_voice(guild: discord.Guild) -> Set[str]:
    """Return watched handles currently presentes em qualquer canal de voz."""
    members_in_voice: Set[str] = set()
    for occupant in guild.members:
        if occupant.voice and occupant.voice.channel:
            key = _identify_watch_key(occupant)
            if key:
                members_in_voice.add(key)
    return members_in_voice


def _resolve_notification_targets(
    guild: discord.Guild,
    watch_members: Dict[str, discord.Member],
) -> List[discord.Member]:
    """Decide which watched members should be notified for a join event."""
    recipients_keys: Set[str] = set(watch_members.keys())
    recipients_keys -= _watched_handles_in_voice(guild)
    return [watch_members[key] for key in recipients_keys if key in watch_members]


async def send_voice_alert(
    member: discord.Member,
    channel: discord.VoiceChannel,
) -> None:
    """Send a notification to the configured alert channel for tracked members."""
    watch_members = _collect_watch_members(channel.guild)
    recipients = _resolve_notification_targets(channel.guild, watch_members)

    if not recipients:
        logging.info(
            "Sem destinatarios para alertar quando %s entrou na call %s",
            member,
            channel,
        )
        return

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

    mention_targets = " ".join(target.mention for target in recipients)

    embed = discord.Embed(
        title="Player em call",
        description=(
            f"{member.mention} entrou na call {channel.mention}.\n"
            f"Avisar: {mention_targets}"
        ),
        color=discord.Color.green(),
    )
    embed.set_footer(text="Watcher Bot")

    await alert_channel.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions(users=True),
    )


@bot.event
async def on_voice_state_update(
    member: discord.Member,
    before: discord.VoiceState,
    after: discord.VoiceState,
) -> None:
    """Trigger when someone joins a voice channel."""
    if member.bot:
        return

    # Avisos apenas quando o usuario estava desconectado e entrou em um canal.
    if after.channel is None or before.channel is not None:
        return

    member_watch_key = _identify_watch_key(member)
    if not member_watch_key:
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

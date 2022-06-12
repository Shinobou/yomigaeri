import re
import typing

import hikari


SNOWFLAKE_REGEX: typing.Final[re.Pattern[str]] = re.compile(r"<@!?(\d+)>")


async def _convert_to_member(event: hikari.MessageCreateEvent, gateway_bot: hikari.GatewayBot, argument: str) -> hikari.Member | None:
    if not event.message.guild_id:
        return None

    guild: hikari.GatewayGuild | None = gateway_bot.cache.get_guild(event.message.guild_id)

    if not guild:
        return None

    try:
        user_id: int = int(SNOWFLAKE_REGEX.findall(argument)[0])
        return guild.get_member(user_id)
    except Exception:
        pass

    if argument.isnumeric():
        return guild.get_member(int(argument))
    else:
        if members := await gateway_bot.rest.search_members(guild, argument):
            return members[0]

    return None

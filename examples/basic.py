import logging
import os

import hikari
import yomigaeri

bot: yomigaeri.Bot = yomigaeri.Bot("!", os.environ.get("DISCORD_TOKEN"))


@bot.listen(hikari.StartedEvent)
async def on_started_event(_: hikari.StartedEvent) -> None:
    logging.info("Bot is online!")


@bot.command("ping", "Checks the latency of the bot.")
async def on_ping_command(event: hikari.MessageCreateEvent) -> None:
    await event.message.respond(f"Latency: {bot._gateway_bot.heartbeat_latency * 1000:.1f} ms")


@bot.command("add", "Adds two numbers together.")
async def on_add_command(event: hikari.MessageCreateEvent, first_number: float, second_number: float) -> None:
    await event.message.respond(f"{first_number} + {second_number} = {first_number + second_number}")


bot.run()

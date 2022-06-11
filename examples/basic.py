import os

import hikari

from yomigaeri import Bot

bot = Bot("!", os.environ.get("DISCORD_TOKEN"))


@bot.command("test", "tests")
async def command(event: hikari.MessageCreateEvent) -> None:
    await event.message.respond("Hey")


@bot.listen(hikari.StartedEvent)
async def on_started_event(_: hikari.StartedEvent) -> None:
    print("ONLINE!!!")


bot.run()

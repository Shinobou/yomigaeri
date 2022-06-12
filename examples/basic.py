import os

import hikari

import yomigaeri
from yomigaeri import Bot

bot = Bot("!", os.environ.get("DISCORD_TOKEN"))


@bot.command("ping", "pong")
async def command(context: yomigaeri.Context) -> None:
    await context.event.message.respond("Pong!")


@bot.command("add", "adds two numbers")
async def add(context: yomigaeri.Context, number_one: int, number_two: int) -> None:
    await context.event.message.respond(number_one + number_two)


@bot.command("hello", "says hello")
async def hello_command(context: yomigaeri.Context, member: hikari.Member) -> None:
    await context.event.message.respond(f"Hello, {member.mention}!")


@bot.listen(hikari.StartedEvent)
async def on_started_event(_: hikari.StartedEvent) -> None:
    print("ONLINE!")


bot.run()

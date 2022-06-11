import typing

import hikari

from yomigaeri.command import Command


class Bot(object):
    def __init__(self, prefix: str, token: str) -> None:
        """Represents the Discord bot.

        :param prefix: the prefix that triggers commands.
        :param token: the bots Discord token.
        """
        self.prefix: str = prefix
        self.token: str = token
        self.commands: list[Command] = []

        self._gateway_bot: hikari.GatewayBot = hikari.GatewayBot(self.token)

    def command(
        self, name: str, description: str
    ) -> typing.Callable[
        [
            typing.Callable[
                [hikari.Event], typing.Coroutine[typing.Any, typing.Any, None]
            ]
        ],
        typing.Callable[[hikari.Event], typing.Coroutine[typing.Any, typing.Any, None]],
    ]:
        """Adds a command to the bot.

        :param name: the name of the command.
        :param description: the description of the command.

        :return: typing.Callable[[typing.Callable[[hikari.Event], typing.Coroutine[typing.Any, typing.Any, None]]],typing.Callable[[hikari.Event], typing.Coroutine[typing.Any, typing.Any, None]],]
        """

        def _inner(
            callback: typing.Callable[
                [hikari.Event], typing.Coroutine[typing.Any, typing.Any, None]
            ]
        ) -> typing.Callable[
            [hikari.Event], typing.Coroutine[typing.Any, typing.Any, None]
        ]:
            self.commands.append(Command(name, description, callback))
            return callback

        return _inner

    def listen(
        self, event: type
    ) -> typing.Callable[
        [typing.Callable[[typing.Any], typing.Coroutine[typing.Any, typing.Any, None]]],
        typing.Callable[[typing.Any], typing.Coroutine[typing.Any, typing.Any, None]],
    ]:
        """Adds an event listener to the bot.

        :param event: the type of event
        :return: typing.Callable[[typing.Callable[[typing.Any], typing.Coroutine[typing.Any, typing.Any, None]]],typing.Callable[[typing.Any], typing.Coroutine[typing.Any, typing.Any, None]],
        """

        def inner(
            callback: typing.Callable[
                [typing.Any], typing.Coroutine[typing.Any, typing.Any, None]
            ]
        ) -> typing.Callable[
            [typing.Any], typing.Coroutine[typing.Any, typing.Any, None]
        ]:
            self._gateway_bot.event_manager.subscribe(event, callback)
            return callback

        return inner

    async def _on_message_create_event(self, event: hikari.MessageCreateEvent) -> None:
        for command in self.commands:
            if event.message.content is not None:
                if event.message.content.startswith(self.prefix + command.name):
                    await command.callback(event)

    def run(self) -> None:
        """Runs the bot."""
        self._gateway_bot.event_manager.subscribe(
            hikari.MessageCreateEvent, self._on_message_create_event
        )
        self._gateway_bot.run()

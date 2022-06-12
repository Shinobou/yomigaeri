import inspect
import types
import typing

import hikari

from yomigaeri.command import Command
from yomigaeri.context import Context
from yomigaeri.converters import _convert_to_member


class Bot(object):
    """Represents the Discord Bot.

    Attributes:
        prefix (str): the prefix that will trigger the bot to activate a command.
        token (str): the bots Discord token.
        commands (list[Command]): the list of bot commands.
        gateway_bot (hikari.GatewayBot): the gateway bot.
    """

    def __init__(self, prefix: str, token: str) -> None:
        """Initializes the Bot object

        Args:
            prefix (str): the prefix that will trigger the bot to activate a command.
            token (str): the bots Discord token.
        """
        self.prefix: str = prefix
        self.token: str = token
        self.commands: list[Command] = []
        self.gateway_bot: hikari.GatewayBot = hikari.GatewayBot(self.token)

    def command(
        self, name: str, description: str
    ) -> typing.Callable[
        [typing.Callable[..., typing.Coroutine[typing.Any, typing.Any, None]]],
        typing.Callable[[hikari.Event], typing.Coroutine[typing.Any, typing.Any, None]],
    ]:
        """Adds a command to the bot.

        Args:
            name (str): the name of the command
            description (str): the description of the command

        Returns:
            typing.Callable[
                [
                    typing.Callable[
                        [hikari.Event], typing.Coroutine[typing.Any, typing.Any, None]
                    ]
                ],
                typing.Callable[[hikari.Event], typing.Coroutine[typing.Any, typing.Any, None]],
            ]
        """

        def _inner(
            callback: typing.Callable[
                [hikari.Event], typing.Coroutine[typing.Any, typing.Any, None]
            ]
        ) -> typing.Callable[
            [hikari.Event], typing.Coroutine[typing.Any, typing.Any, None]
        ]:
            signature: inspect.Signature = inspect.signature(callback)
            parameters: types.MappingProxyType[
                str, inspect.Parameter
            ] = signature.parameters
            arguments: list[tuple[str, type]] = [
                (key, parameters[key].annotation) for key in parameters.keys()
            ]
            arguments.pop(0)
            self.commands.append(Command(name, description, callback, arguments))
            return callback

        return _inner

    def listen(
        self, event: type
    ) -> typing.Callable[
        [typing.Callable[[typing.Any], typing.Coroutine[typing.Any, typing.Any, None]]],
        typing.Callable[[typing.Any], typing.Coroutine[typing.Any, typing.Any, None]],
    ]:
        """Adds an event listener to the bot.

        Args:
            event (type): the type of event.

        Returns:
            typing.Callable[
                [typing.Callable[[typing.Any], typing.Coroutine[typing.Any, typing.Any, None]]],
                typing.Callable[[typing.Any], typing.Coroutine[typing.Any, typing.Any, None]],
            ]
        """

        def inner(
            callback: typing.Callable[
                [typing.Any], typing.Coroutine[typing.Any, typing.Any, None]
            ]
        ) -> typing.Callable[
            [typing.Any], typing.Coroutine[typing.Any, typing.Any, None]
        ]:
            self.gateway_bot.event_manager.subscribe(event, callback)
            return callback

        return inner

    async def _convert_arguments(
        self, event: hikari.MessageCreateEvent, arguments: list[str], command_arguments: list[tuple[str, type]]
    ) -> dict[str, typing.Any]:
        arguments_dict: dict[str, typing.Any] = {}

        for x in range(len(arguments)):
            argument_type: type = command_arguments[x][1]
            argument: str = arguments[x]
            if argument_type in (str, int, float):
                arguments_dict[command_arguments[x][0]] = argument_type(
                    argument
                )
            elif argument_type is hikari.Member:
                arguments_dict[command_arguments[x][0]] = await _convert_to_member(event, self.gateway_bot, argument)

        return arguments_dict

    async def _on_message_create_event(self, event: hikari.MessageCreateEvent) -> None:
        for command in self.commands:
            if event.message.content is not None:
                if event.message.content.startswith(self.prefix + command.name):
                    if command.arguments is None:
                        await command.callback(event)
                    else:
                        arguments: list[str] = event.message.content.split(" ")
                        arguments.pop(0)
                        if len(arguments) != len(command.arguments):
                            return
                        await command.callback(
                            Context(event, self.gateway_bot),
                            **await self._convert_arguments(event, arguments, command.arguments)
                        )
                    return

    def run(self) -> None:
        """Runs the bot."""
        self.gateway_bot.event_manager.subscribe(
            hikari.MessageCreateEvent, self._on_message_create_event
        )
        self.gateway_bot.run()

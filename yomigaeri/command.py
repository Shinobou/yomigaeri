import typing
from dataclasses import dataclass

import hikari


@dataclass
class Command(object):
    name: str
    description: str
    callback: typing.Callable[
        [hikari.Event], typing.Coroutine[typing.Any, typing.Any, None]
    ]

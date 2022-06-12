import typing
from dataclasses import dataclass


@dataclass
class Command(object):
    name: str
    description: str
    callback: typing.Callable[..., typing.Coroutine[typing.Any, typing.Any, None]]
    arguments: typing.Optional[list[tuple[str, type]]]

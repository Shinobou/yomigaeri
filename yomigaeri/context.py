from dataclasses import dataclass

import hikari


@dataclass
class Context(object):
    event: hikari.MessageCreateEvent
    gateway_bot: hikari.GatewayBot

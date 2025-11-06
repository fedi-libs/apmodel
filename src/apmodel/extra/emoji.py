from typing import ClassVar

from ..core.object import Object


class Emoji(Object):
    AS_URI: ClassVar[str] = "http://joinmastodon.org/ns#Emoji"
from typing import ClassVar

from ..core.link import Link


class Mention(Link):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Mention"

from typing import ClassVar

from ..core import Link


class Hashtag(Link):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Hashtag"
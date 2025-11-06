from typing import ClassVar

from ..core.object import Object


class Article(Object):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Article"

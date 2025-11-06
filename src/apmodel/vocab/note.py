from typing import ClassVar

from ..core.object import Object


class Note(Object):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Note"

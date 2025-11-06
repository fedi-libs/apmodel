from typing import ClassVar

from ..core.object import Object


class Document(Object):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Document"


class Audio(Document):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Audio"


class Image(Document):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Image"


class Video(Document):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Video"


class Page(Document):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Page"

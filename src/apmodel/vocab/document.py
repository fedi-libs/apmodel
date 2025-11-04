from pydantic import Field

from ..core.object import Object


class Document(Object):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Document",
        kw_only=True,
        alias="@type",
    )

class Audio(Document):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Audio",
        kw_only=True,
        alias="@type",
    )

class Image(Document):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Image",
        kw_only=True,
        alias="@type",
    )

class Video(Document):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Video",
        kw_only=True,
        alias="@type",
    )

class Page(Document):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Page",
        kw_only=True,
        alias="@type",
    )

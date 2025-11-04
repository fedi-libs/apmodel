from pydantic import Field

from ..core.object import Object


class Note(Object):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Note",
        kw_only=True,
        alias="@type",
    )

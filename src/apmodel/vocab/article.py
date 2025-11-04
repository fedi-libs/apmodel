from pydantic import Field

from ..core.object import Object


class Article(Object):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Article",
        kw_only=True,
        alias="@type",
    )

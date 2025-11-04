from __future__ import annotations

from pydantic import Field

from ..core import Object


class Emoji(Object):
    type: str = Field(
        alias="@type",
        default="http://joinmastodon.org/ns#Emoji",
        kw_only=True,
    )

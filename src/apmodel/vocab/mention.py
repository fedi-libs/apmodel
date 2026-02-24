from typing import Optional

from pydantic import Field

from ..core.link import Link


class Mention(Link):
    type: str = Field(default="Mention", kw_only=True, frozen=True)

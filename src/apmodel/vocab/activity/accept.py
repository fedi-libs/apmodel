from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Accept(Activity):
    type: str = Field(default="Accept", kw_only=True, frozen=True)


class TentativeAccept(Accept):
    type: str = Field(default="TentativeAccept", kw_only=True, frozen=True)

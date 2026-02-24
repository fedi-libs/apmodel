from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Move(Activity):
    type: str = Field(default="Move", kw_only=True, frozen=True)

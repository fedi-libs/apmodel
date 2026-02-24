from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Flag(Activity):
    type: str = Field(default="Flag", kw_only=True, frozen=True)

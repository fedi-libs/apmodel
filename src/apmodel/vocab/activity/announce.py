from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Announce(Activity):
    type: str = Field(default="Announce", kw_only=True, frozen=True)

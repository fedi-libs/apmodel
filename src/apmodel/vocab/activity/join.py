from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Join(Activity):
    type: str = Field(default="Join", kw_only=True, frozen=True)

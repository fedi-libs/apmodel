from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Remove(Activity):
    type: str = Field(default="Remove", kw_only=True, frozen=True)

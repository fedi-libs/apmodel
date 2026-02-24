from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Read(Activity):
    type: str = Field(default="Read", kw_only=True, frozen=True)

from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Create(Activity):
    type: str = Field(default="Create", kw_only=True, frozen=True)

from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Listen(Activity):
    type: str = Field(default="Listen", kw_only=True, frozen=True)

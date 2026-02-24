from typing import Optional

from pydantic import Field

from ...core.activity import IntransitiveActivity


class Travel(IntransitiveActivity):
    type: str = Field(default="Travel", kw_only=True, frozen=True)

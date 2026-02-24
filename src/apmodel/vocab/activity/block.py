from typing import Optional

from pydantic import Field

from .ignore import Ignore


class Block(Ignore):
    type: str = Field(default="Block", kw_only=True, frozen=True)

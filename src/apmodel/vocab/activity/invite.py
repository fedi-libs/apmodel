from typing import Optional

from pydantic import Field

from .offer import Offer


class Invite(Offer):
    type: str = Field(default="Invite", kw_only=True, frozen=True)

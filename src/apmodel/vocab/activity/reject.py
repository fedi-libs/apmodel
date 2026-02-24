from typing import Optional

from pydantic import Field

from ...core.activity import Activity


class Reject(Activity):
    type: str = Field(default="Reject", kw_only=True, frozen=True)


class TentativeReject(Reject):
    type: str = Field(default="TentativeReject", kw_only=True, frozen=True)

from __future__ import annotations

from typing import Optional, TypeVar

from pydantic import Field

from ..context import LDContext
from ..types import ActivityPubModel

T = TypeVar("T", bound="Link")


class Link(ActivityPubModel):
    context: LDContext = Field(
        default_factory=lambda: LDContext(["https://www.w3.org/ns/activitystreams"]),
        kw_only=True,
        alias="@context",
    )

    type: str = Field(default="Link", kw_only=True, frozen=True)
    id: Optional["str | Link"] = Field(default=None, kw_only=True)
    name: Optional[str] = Field(default=None, kw_only=True)
    href: Optional[str] = Field(default=None)
    hreflang: Optional[str] = Field(default=None)
    media_type: Optional[str] = Field(default=None)

from __future__ import annotations

from typing import Optional, Union

import msgspec
from ..types import ActivityPubModel


class Link(ActivityPubModel):
    type: Optional[str] = msgspec.field(default="Link")
    id: Optional[str] = msgspec.field(default=None)
    href: Optional[str] = msgspec.field(default=None)
    rel: Optional[Union[str, list[str]]] = msgspec.field(default=None)
    media_type: Optional[str] = msgspec.field(default=None)
    name: Optional[str] = msgspec.field(default=None)
    hreflang: Optional[str] = msgspec.field(default=None)
    height: Optional[int] = msgspec.field(default=None)
    width: Optional[int] = msgspec.field(default=None)
    preview: Optional[Union[str, Link]] = msgspec.field(default=None)

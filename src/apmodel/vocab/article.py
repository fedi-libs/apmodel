from typing import Optional

from pydantic import Field

from ..core.object import Object


class Article(Object[str | None]):
    type: str = Field(default="Article", kw_only=True, frozen=True)

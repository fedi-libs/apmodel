from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Optional, Union

from pydantic import BeforeValidator, Field

from ..context import LDContext
from ..helpers import get_value_from_array
from ..types import ActivityPubModel, parse_ld_context

if TYPE_CHECKING:
    from .object import Object


class Link(ActivityPubModel):
    context: Annotated[LDContext, BeforeValidator(parse_ld_context)] = Field(
        alias="@context",
        kw_only=True,
        default_factory=lambda: LDContext(
            ["https://www.w3.org/ns/activitystreams"]
        ),
    )

    type: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field(default="Link")
    )
    id: Annotated[
        Optional[Union[str, "Object", "Link"]],
        BeforeValidator(get_value_from_array),
    ] = Field()
    name: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field()
    )
    href: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field()
    )
    hreflang: Annotated[
        Optional[str], BeforeValidator(get_value_from_array)
    ] = Field()
    mediaType: Annotated[
        Optional[str], BeforeValidator(get_value_from_array)
    ] = Field()
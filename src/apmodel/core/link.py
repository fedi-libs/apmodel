from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, ClassVar

from pydantic import BeforeValidator, Field

from apmodel.types.aliases import ID_OPT_STR_OR_OBJECT_OR_LINK, OPT_STR

from ..context import LDContext
from ..helpers import generate_aliases, parse_ld_context
from ..types import ActivityPubModel

if TYPE_CHECKING:
    pass


class Link(ActivityPubModel):
    context: Annotated[LDContext, BeforeValidator(parse_ld_context)] = Field(
        alias="@context",
        kw_only=True,
        default_factory=lambda: LDContext(
            ["https://www.w3.org/ns/activitystreams"]
        ),
    )
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Link"

    id: ID_OPT_STR_OR_OBJECT_OR_LINK = Field(
        validation_alias="@id", serialization_alias="@id"
    )
    name: OPT_STR = Field(default=None, **generate_aliases("name", "as2"))
    href: OPT_STR = Field(default=None, **generate_aliases("href", "as2"))
    href_lang: OPT_STR = Field(
        default=None, **generate_aliases("hreflang", "as2")
    )
    media_type: OPT_STR = Field(
        default=None, **generate_aliases("mediaType", "as2")
    )

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List, Optional, TypeVar, Union

from pydantic import BeforeValidator, Field

from ..context import LDContext
from ..helpers import get_value_from_array

# from ..dumper import _serialize_model_to_json
from ..types import ActivityPubModel, parse_ld_context

if TYPE_CHECKING:
    from ..extra.emoji import Emoji
    from ..extra.hashtag import Hashtag
    from ..extra.schema import PropertyValue
    from ..vocab.actor import Actor
    from ..vocab.document import Image
    from .collection import Collection
    from .link import Link

T = TypeVar("T", bound="Object")


class Object(ActivityPubModel):
    context: Annotated[LDContext, BeforeValidator(parse_ld_context)] = Field(
        alias="@context",
        kw_only=True,
        default_factory=lambda: LDContext(
            ["https://www.w3.org/ns/activitystreams"]
        ),
    )
    id: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = Field(
        validation_alias="@id", serialization_alias="@id", default=None
    )
    type: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field(
            alias="@type",
            default="https://www.w3.org/ns/activitystreams#Object",
            kw_only=True,
        )
    )
    name: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field(
            validation_alias="https://www.w3.org/ns/activitystreams#name",
            serialization_alias="https://www.w3.org/ns/activitystreams#name",
            default=None,
        )
    )
    content: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field(
            validation_alias="https://www.w3.org/ns/activitystreams#content",
            serialization_alias="https://www.w3.org/ns/activitystreams#content",
            default=None,
        )
    )
    summary: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field(
            alias="https://www.w3.org/ns/activitystreams#summary", default=None
        )
    )
    url: Annotated[
        Optional[Union[str, "Link"]], BeforeValidator(get_value_from_array)
    ] = Field(alias="https://www.w3.org/ns/activitystreams#url", default=None)
    published: Annotated[
        Optional[datetime], BeforeValidator(get_value_from_array)
    ] = Field(
        alias="https://www.w3.org/ns/activitystreams#published", default=None
    )
    updated: Annotated[
        Optional[datetime], BeforeValidator(get_value_from_array)
    ] = Field(
        alias="https://www.w3.org/ns/activitystreams#updated", default=None
    )
    attributed_to: Annotated[
        Optional[Union[str, "Actor", List[Union[str, "Actor"]]]],
        BeforeValidator(get_value_from_array),
    ] = Field(
        alias="https://www.w3.org/ns/activitystreams#attributedTo", default=None
    )
    audience: Annotated[
        Optional[Union[str, "Object", List[Union[str, "Object"]]]],
        BeforeValidator(get_value_from_array),
    ] = Field(
        alias="https://www.w3.org/ns/activitystreams#audience", default=None
    )
    to: Annotated[
        Optional[Union[str, "Object", List[Union[str, "Object"]]]],
        BeforeValidator(get_value_from_array),
    ] = Field(alias="https://www.w3.org/ns/activitystreams#to", default=None)
    bto: Annotated[
        Optional[Union[str, "Object", List[Union[str, "Object"]]]],
        BeforeValidator(get_value_from_array),
    ] = Field(alias="https://www.w3.org/ns/activitystreams#bto", default=None)
    cc: Annotated[
        Optional[Union[str, "Object", List[Union[str, "Object"]]]],
        BeforeValidator(get_value_from_array),
    ] = Field(alias="https://www.w3.org/ns/activitystreams#cc", default=None)
    bcc: Annotated[
        Optional[Union[str, "Object", List[Union[str, "Object"]]]],
        BeforeValidator(get_value_from_array),
    ] = Field(alias="https://www.w3.org/ns/activitystreams#bcc", default=None)
    generator: Annotated[
        Optional["Object"], BeforeValidator(get_value_from_array)
    ] = Field(
        alias="https://www.w3.org/ns/activitystreams#generator", default=None
    )
    icon: Annotated[
        Optional["Image"], BeforeValidator(get_value_from_array)
    ] = Field(alias="https://www.w3.org/ns/activitystreams#icon", default=None)
    image: Annotated[
        Optional["Image"], BeforeValidator(get_value_from_array)
    ] = Field(alias="https://www.w3.org/ns/activitystreams#image", default=None)
    in_reply_to: Annotated[
        Optional["Object"], BeforeValidator(get_value_from_array)
    ] = Field(
        alias="https://www.w3.org/ns/activitystreams#inReplyTo", default=None
    )
    location: Annotated[
        Optional["Object"], BeforeValidator(get_value_from_array)
    ] = Field(
        alias="https://www.w3.org/ns/activitystreams#location", default=None
    )
    preview: Annotated[
        Optional["Object"], BeforeValidator(get_value_from_array)
    ] = Field(
        alias="https://www.w3.org/ns/activitystreams#preview", default=None
    )
    replies: Annotated[
        Optional["Collection"], BeforeValidator(get_value_from_array)
    ] = Field(
        alias="https://www.w3.org/ns/activitystreams#replies", default=None
    )
    scope: Annotated[
        Optional["Object"], BeforeValidator(get_value_from_array)
    ] = Field(alias="https://www.w3.org/ns/activitystreams#scope", default=None)
    tag: Annotated[
        List[Union["Object", "Hashtag", "Emoji"]],
        BeforeValidator(get_value_from_array),
    ] = Field(
        alias="https://www.w3.org/ns/activitystreams#tag", default_factory=list
    )
    attachment: Annotated[
        List[Union["Object", "PropertyValue"]],
        BeforeValidator(get_value_from_array),
    ] = Field(
        alias="https://www.w3.org/ns/activitystreams#attachment",
        default_factory=list,
    )
    #    _extra: dict = Field(default_factory=dict)

    # def to_json(self):
    #    return _serialize_model_to_json(self)

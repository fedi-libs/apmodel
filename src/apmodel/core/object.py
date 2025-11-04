from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, List, Optional, TypeVar, Union

from pydantic import BeforeValidator, ConfigDict, Field

from apmodel.types.aliases import (
    JSONLD_CONTEXT,
    OPT_DATETIME,
    OPT_STR,
    OPT_STR_OR_LINK,
)

from ..context import LDContext
from ..helpers import generate_aliases, get_value_from_array

# from ..dumper import _serialize_model_to_json
from ..types import ActivityPubModel

if TYPE_CHECKING:
    from ..extra.emoji import Emoji
    from ..extra.hashtag import Hashtag
    from ..extra.schema import PropertyValue
    from ..vocab.actor import Actor
    from ..vocab.document import Image
    from .collection import Collection

T = TypeVar("T", bound="Object")


class Object(ActivityPubModel):
    model_config = ConfigDict(
        serialize_by_alias=True 
    )
    
    context: JSONLD_CONTEXT = Field(
        validation_alias="@context",
        serialization_alias="@context",
        kw_only=True,
        default_factory=lambda: LDContext(
            ["https://www.w3.org/ns/activitystreams"]
        ),
    )
    id: OPT_STR = Field(
        validation_alias="@id", serialization_alias="@id", default=None
    )
    type: Annotated[str, BeforeValidator(get_value_from_array)] = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Object",
        kw_only=True,
    )
    name: OPT_STR = Field(default=None, **generate_aliases("name", "as2"))
    content: OPT_STR = Field(default=None, **generate_aliases("content", "as2"))
    summary: OPT_STR = Field(
        alias="https://www.w3.org/ns/activitystreams#summary", default=None
    )
    url: OPT_STR_OR_LINK = Field(
        alias="https://www.w3.org/ns/activitystreams#url", default=None
    )
    published: OPT_DATETIME = Field(
        alias="https://www.w3.org/ns/activitystreams#published", default=None
    )
    updated: OPT_DATETIME = Field(
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

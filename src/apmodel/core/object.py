from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, TypeVar, Union, Dict

import msgspec
from ..context import LDContext
from ..types import ActivityPubModel

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
    context: LDContext = msgspec.field(
        default_factory=lambda: LDContext(["https://www.w3.org/ns/activitystreams"]),
        name="@context",
    )
    id: Optional[str] = msgspec.field(default=None)
    type: Optional[str] = msgspec.field(default="Object")
    name: Optional[str] = msgspec.field(default=None)
    content: Optional[str] = msgspec.field(default=None)
    summary: Optional[str] = msgspec.field(default=None)
    url: Optional[Union[str, Link]] = msgspec.field(default=None)
    published: Optional[str] = msgspec.field(default=None)
    updated: Optional[str] = msgspec.field(default=None)
    attributed_to: Optional[Union[str, Actor, List[Union[str, Actor]]]] = msgspec.field(
        default=None
    )
    audience: Optional[Union[str, Object, Dict[str, Any], List[Union[str, Object]]]] = (
        msgspec.field(default=None)
    )
    to: Optional[
        Union[str, Object, Dict[str, Any], List[Union[str, Object, Dict[str, Any]]]]
    ] = msgspec.field(default=None)
    bto: Optional[
        Union[str, Object, Dict[str, Any], List[Union[str, Object, Dict[str, Any]]]]
    ] = msgspec.field(default=None)
    cc: Optional[
        Union[str, Object, Dict[str, Any], List[Union[str, Object, Dict[str, Any]]]]
    ] = msgspec.field(default=None)
    bcc: Optional[
        Union[str, Object, Dict[str, Any], List[Union[str, Object, Dict[str, Any]]]]
    ] = msgspec.field(default=None)
    generator: Optional[Union[Object, Dict[str, Any]]] = msgspec.field(default=None)
    icon: Optional[Image] = msgspec.field(default=None)
    image: Optional[Image] = msgspec.field(default=None)
    in_reply_to: Optional[Union[Object, Dict[str, Any]]] = msgspec.field(default=None)
    location: Optional[Union[Object, Dict[str, Any]]] = msgspec.field(default=None)
    preview: Optional[Union[Object, Dict[str, Any]]] = msgspec.field(default=None)
    replies: Optional[Collection] = msgspec.field(default=None)
    likes: Optional[Collection] = msgspec.field(default=None)
    shares: Optional[Collection] = msgspec.field(default=None)
    scope: Optional[Union[Object, Dict[str, Any]]] = msgspec.field(default=None)
    tag: List[Union[Object, Hashtag, Emoji, Link, Dict[str, Any]]] = msgspec.field(
        default_factory=list
    )
    attachment: List[Union[PropertyValue, Dict[str, Any], Object, Link]] = (
        msgspec.field(default_factory=list)
    )

    @classmethod
    def _convert_field_to_model(cls, v: Any, ld_context: Any = None) -> Any:
        from ..loader import load

        if v is None:
            return None
        return load(v, "raw", parent_context=ld_context)

    @classmethod
    def model_validate(
        cls: type[T], data: Any, context: Optional[Dict[str, Any]] = None
    ) -> T:
        if not isinstance(data, dict):
            if isinstance(data, cls):
                return data
            raise ValueError(f"Expected dict, got {type(data)}")

        ld_context = context.get("ld_context") if context else None

        # Pre-process fields that need conversion
        data_copy = data.copy()
        fields_to_validate = [
            "url",
            "attributedTo",
            "audience",
            "to",
            "bto",
            "cc",
            "bcc",
            "generator",
            "icon",
            "image",
            "inReplyTo",
            "location",
            "preview",
            "replies",
            "likes",
            "shares",
            "scope",
            "tag",
            "attachment",
        ]
        for field in fields_to_validate:
            if field in data_copy:
                data_copy[field] = cls._convert_field_to_model(
                    data_copy[field], ld_context
                )

        return super().model_validate(data_copy, context=context)

    def _inference_context(self, result: dict) -> Dict[str, Any]:
        res_ctx = result.get("@context", [])
        dynamic_context = LDContext(res_ctx)
        dynamic_context.add("https://www.w3.org/ns/activitystreams")

        if result.get("sensitive"):
            dynamic_context.add({"sensitive": "as:sensitive"})

        tootcontext = {"toot": "http://joinmastodon.org/ns#"}

        if result.get("featured"):
            dynamic_context.add({**tootcontext, "featured": "toot:featured"})
        if result.get("featuredTags"):
            dynamic_context.add({**tootcontext, "featuredTags": "toot:featuredTags"})
        if result.get("indexable"):
            dynamic_context.add({**tootcontext, "indexable": "toot:indexable"})
        if result.get("discoverable"):
            dynamic_context.add({**tootcontext, "discoverable": "toot:discoverable"})

        if any(
            isinstance(item, dict) and item.get("type") == "PropertyValue"
            for item in result.get("attachment", [])
        ):
            dynamic_context.add(
                {
                    "schema": "http://schema.org#",
                    "value": "schema:value",
                    "PropertyValue": "schema:PropertyValue",
                }
            )
        if any(
            isinstance(item, (dict, ActivityPubModel))
            and getattr(item, "type", None) == "Emoji"
            for item in result.get("tag", [])
        ):
            dynamic_context.add({**tootcontext, "Emoji": "toot:Emoji"})

        if any(
            isinstance(item, (dict, ActivityPubModel))
            and getattr(item, "type", None) == "Hashtag"
            for item in result.get("tag", [])
        ):
            dynamic_context.add(
                {"Hashtag": "https://www.w3.org/ns/activitystreams#Hashtag"}
            )

        finalcontext = dynamic_context.full_context
        if finalcontext:
            result["@context"] = finalcontext

        return result

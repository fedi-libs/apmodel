from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, List, Optional, TypeVar

from pydantic import Field, ValidationInfo, field_validator
from typing_extensions import Dict

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
T_id = TypeVar("T_id", str, Optional[str])


class Object(ActivityPubModel, Generic[T_id]):
    context: LDContext = Field(
        default_factory=lambda: LDContext(
            ["https://www.w3.org/ns/activitystreams"]
        ),
        kw_only=True,
        alias="@context",
    )
    id: T_id = Field(default=None)  # pyrefly: ignore[bad-assignment]
    type: str = Field(default="Object", kw_only=True, frozen=True)
    name: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    url: Optional["str | Link"] = Field(default=None)
    published: Optional[str] = Field(default=None)
    updated: Optional[str] = Field(default=None)
    attributed_to: Optional["str | Actor | List[str | Actor]"] = Field(
        default=None
    )
    audience: Optional["str | Object | Dict[str, Any] | List[str | Object]"] = (
        Field(default=None)
    )
    to: Optional[
        "str | Object | Dict[str, Any] | List[str | Object | Dict[str, Any]]"
    ] = Field(default=None)
    bto: Optional[
        "str | Object | Dict[str, Any] | List[str | Object | Dict[str, Any]]"
    ] = Field(default=None)
    cc: Optional[
        "str | Object | Dict[str, Any] | List[str | Object | Dict[str, Any]]"
    ] = Field(default=None)
    bcc: Optional[
        "str | Object | Dict[str, Any] | List[str | Object | Dict[str, Any]]"
    ] = Field(default=None)
    generator: "Optional[Object | Dict[str, Any]]" = Field(default=None)
    icon: Optional["Image"] = Field(default=None)
    image: Optional["Image"] = Field(default=None)
    in_reply_to: "Optional[Object | Dict[str, Any]]" = Field(default=None)
    location: "Optional[Object | Dict[str, Any]]" = Field(default=None)
    preview: "Optional[Object | Dict[str, Any]]" = Field(default=None)
    replies: Optional["Collection"] = Field(default=None)
    likes: Optional["Collection"] = Field(default=None)
    shares: Optional["Collection"] = Field(default=None)
    scope: "Optional[Object | Dict[str, Any]]" = Field(default=None)
    tag: "List[Object | Hashtag | Emoji | Link | Dict[str, Any]]" = Field(
        default_factory=list
    )
    attachment: "List[PropertyValue | Dict[str, Any] | Object | Link]" = Field(
        default_factory=list
    )

    @classmethod
    def _convert_field_to_model(cls, v: Any, info: ValidationInfo) -> Any:
        from ..loader import load

        if v is None:
            return None
        parent_context = (
            info.context.get("ld_context") if info.context else None
        )
        return load(v, "raw", parent_context=parent_context)

    @field_validator(
        "url",
        "attributed_to",
        "audience",
        "to",
        "bto",
        "cc",
        "bcc",
        "generator",
        "icon",
        "image",
        "in_reply_to",
        "location",
        "preview",
        "replies",
        "likes",
        "shares",
        "scope",
        "tag",
        "attachment",
        mode="before",
    )
    @classmethod
    def validate_fields(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

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
            dynamic_context.add(
                {**tootcontext, "featuredTags": "toot:featuredTags"}
            )
        if result.get("indexable"):
            dynamic_context.add({**tootcontext, "indexable": "toot:indexable"})
        if result.get("discoverable"):
            dynamic_context.add(
                {**tootcontext, "discoverable": "toot:discoverable"}
            )

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
            isinstance(item, dict) and item.get("type") == "Emoji"
            for item in result.get("tag", [])
        ):
            dynamic_context.add({**tootcontext, "Emoji": "toot:Emoji"})

        if any(
            isinstance(item, dict) and item.get("type") == "Hashtag"
            for item in result.get("tag", [])
        ):
            dynamic_context.add(
                {"Hashtag": "https://www.w3.org/ns/activitystreams#Hashtag"}
            )

        finalcontext = dynamic_context.full_context
        if finalcontext:
            result["@context"] = finalcontext

        return result

from __future__ import annotations

from typing import Any, List, Optional, cast

from pydantic import Field, field_validator
from typing_extensions import Dict

from .link import Link
from .object import Object


class Collection(Object[str | None]):
    type: str = Field(default="Collection", kw_only=True)

    total_items: Optional[int] = Field(default=None, ge=0)
    current: Optional[str | CollectionPage | OrderedCollectionPage | Link] = Field(
        default=None
    )
    first: Optional[str | CollectionPage | OrderedCollectionPage | Link] = Field(
        default=None
    )
    last: Optional[str | CollectionPage | OrderedCollectionPage | Link] = Field(
        default=None
    )
    items: Optional[List[Object | Link | Dict[str, Any]]] = Field(default=None)

    @field_validator("current", "first", "last", mode="before")
    @classmethod
    def validate_field(
        cls, v: Optional[str | Dict[str, Any]]
    ) -> Optional[str | CollectionPage | Link]:
        from ..loader import load

        if not v:
            return None
        return cast(Optional[str | CollectionPage | Link], load(v, "raw"))

    @field_validator("items")
    @classmethod
    def validate_items(
        cls, v: Optional[List[Dict[str, Any]]]
    ) -> Optional[List[Object | Link | Dict[str, Any]]]:
        from ..loader import load

        if not v:
            return None
        return cast(Optional[List[Object | Link | Dict[str, Any]]], load(v, "raw"))


class CollectionPage(Collection):
    type: str = Field(default="CollectionPage", kw_only=True)

    part_of: Optional[str | Collection | Link] = Field(default=None)

    next: Optional[str | CollectionPage | Link] = Field(default=None)
    prev: Optional[str | CollectionPage | Link] = Field(default=None)


class OrderedCollection(Collection):
    type: str = Field(default="OrderedCollection", kw_only=True)
    ordered_items: Optional[List[Object | Link | Dict[str, Any] | str]] = Field(
        default=None
    )

    @field_validator("ordered_items")
    @classmethod
    def validate_ordered_items(
        cls, v: Optional[List[Dict[str, Any]]]
    ) -> Optional[List[Object | Link | Dict[str, Any]]]:
        from ..loader import load

        if not v:
            return None
        return cast(Optional[List[Object | Link | Dict[str, Any]]], load(v, "raw"))


class OrderedCollectionPage(OrderedCollection, CollectionPage):
    type: str = Field(default="OrderedCollectionPage", kw_only=True)

    start_index: Optional[int] = Field(default=None, ge=0)

from __future__ import annotations

from typing import ClassVar, List, Optional, Union

from pydantic import Field

from apmodel.helpers import generate_aliases

from .link import Link
from .object import Object


class Collection(Object):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Collection"

    total_items: int = Field(ge=0, **generate_aliases("totalItems", "as2"))
    current: Union[str, dict, Link] = Field(**generate_aliases("current", "as2"))
    first: Optional[Union[str, dict, Link]] = Field(default=None, **generate_aliases("first", "as2"))
    last: Optional[Union[str, dict, Link]] = Field(default=None, **generate_aliases("last", "as2"))
    items: List[Union[Object, Link]] = Field(default_factory=list, **generate_aliases("items", "as2"))
    ordered_items: List[Union[Object, Link]] = Field(default_factory=list, **generate_aliases("orderedItems", "as2"))


class CollectionPage(Collection):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#CollectionPage"

    part_of: Optional[Union[str, Collection, Link]] = Field(default=None, **generate_aliases("partOf", "as2"))

    next: Optional[Union[str, CollectionPage, Link]] = Field(default=None, **generate_aliases("next", "as2"))
    prev: Optional[Union[str, CollectionPage, Link]] = Field(default=None, **generate_aliases("prev", "as2"))


class OrderedCollection(Collection):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#OrderedCollection"


class OrderedCollectionPage(CollectionPage):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#OrderedCollectionPage"
    start_index: Optional[int] = Field(default=None, **generate_aliases("startIndex", "as2"))

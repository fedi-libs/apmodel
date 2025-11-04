from __future__ import annotations

from typing import List, Optional, Union

from pydantic import Field

from .link import Link
from .object import Object


class Collection(Object):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Collection",
        kw_only=True,
    )

    totalItems: Optional[int] = Field(ge=0)
    current: Union[str, dict, Link] = Field()
    first: Optional[Union[str, dict, Link]] = Field()
    last: Optional[Union[str, dict, Link]] = Field()
    items: Optional[List[Union[Object, Link]]] = Field()
    orderedItems: Optional[List[Union[Object, Link]]] = Field()


class CollectionPage(Collection):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#CollectionPage",
        kw_only=True,
    )

    partOf: Optional[Union[str, Collection, Link]] = Field()

    next: Optional[Union[str, CollectionPage, Link]] = Field()
    prev: Optional[Union[str, CollectionPage, Link]] = Field()


class OrderedCollection(Collection):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#OrderedCollection",
        kw_only=True,
    )


class OrderedCollectionPage(CollectionPage):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#OrderedCollectionPage",
        kw_only=True,
    )

    startIndex: Optional[int] = Field()

from __future__ import annotations

from typing import Annotated, List, Optional, Union

from pydantic import BeforeValidator, Field

from ..helpers import get_value_from_array
from .link import Link
from .object import Object


class Collection(Object):
    type: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field(alias="@type", default="https://www.w3.org/ns/activitystreams#Collection", kw_only=True)
    )

    totalItems: Optional[int] = Field(ge=0)
    current: Union[str, dict, Link] = Field()
    first: Optional[Union[str, dict, Link]] = Field()
    last: Optional[Union[str, dict, Link]] = Field()
    items: Optional[List[Union[Object, Link]]] = Field()
    orderedItems: Optional[List[Union[Object, Link]]] = Field()

class CollectionPage(Collection):
    type: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field(
            alias="@type",
            default="https://www.w3.org/ns/activitystreams#CollectionPage",
            kw_only=True,
        )
    )

    partOf: Optional[Union[str, Collection, Link]] = Field()

    next: Optional[Union[str, CollectionPage, Link]] = Field()
    prev: Optional[Union[str, CollectionPage, Link]] = Field()

class OrderedCollection(Collection):
    type: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field(
            alias="@type",
            default="https://www.w3.org/ns/activitystreams#OrderedCollection",
            kw_only=True,
        )
    )

class OrderedCollectionPage(CollectionPage):
    type: Annotated[Optional[str], BeforeValidator(get_value_from_array)] = (
        Field(
            alias="@type",
            default="https://www.w3.org/ns/activitystreams#OrderedCollectionPage",
            kw_only=True,
        )
    )

    startIndex: Optional[int] = Field()

from typing import Annotated, List, Optional, TypeAlias, Union

from pydantic import BeforeValidator, Field

from apmodel.helpers import generate_aliases, get_value_from_array
from apmodel.types.aliases import OPT_BOOLEAN, OPT_STR

from ..core.collection import Collection, OrderedCollection
from ..core.object import Object
from ..extra.cid import Multikey
from ..extra.security import CryptographicKey

ORDERED_COLLECTION: TypeAlias = Annotated[
    Optional[Union[str, OrderedCollection]],
    BeforeValidator(get_value_from_array),
]
COLLECTION: TypeAlias = Annotated[
    Optional[Union[str, Collection]], BeforeValidator(get_value_from_array)
]
COLLECTION_OR_ORDERED_COLLECTION: TypeAlias = Annotated[
    Optional[Union[str, OrderedCollection, Collection]],
    BeforeValidator(get_value_from_array),
]


class ActorEndpoints(Object):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Endpoints",
        kw_only=True,
    )
    sharedInbox: ORDERED_COLLECTION = Field(
        default=None, **generate_aliases("sharedInbox", "as2")
    )


class Actor(Object):
    inbox: ORDERED_COLLECTION = Field(
        default=None, **generate_aliases("inbox", "ldp")
    )
    outbox: ORDERED_COLLECTION = Field(
        default=None, **generate_aliases("outbox", "as2")
    )
    followers: COLLECTION_OR_ORDERED_COLLECTION = Field(
        default=None, **generate_aliases("followers", "as2")
    )
    following: COLLECTION_OR_ORDERED_COLLECTION = Field(
        default=None, **generate_aliases("following", "as2")
    )
    liked: COLLECTION_OR_ORDERED_COLLECTION = Field(
        default=None, **generate_aliases("liked", "as2")
    )
    streams: COLLECTION = Field(
        default=None, **generate_aliases("streams", "as2")
    )
    preferred_username: OPT_STR = Field(
        default=None, **generate_aliases("preferredUsername", "as2")
    )
    endpoints: Annotated[
        Optional[Union[str, ActorEndpoints]],
        BeforeValidator(get_value_from_array),
    ] = Field(default=None, **generate_aliases("endpoints", "as2"))
    discoverable: OPT_BOOLEAN = Field(
        default=None, **generate_aliases("discoverable", "mastodon")
    )
    indexable: OPT_BOOLEAN = Field(
        default=None, **generate_aliases("indexable", "mastodon")
    )
    suspended: OPT_BOOLEAN = Field(
        default=None, **generate_aliases("suspended", "mastodon")
    )
    #    memorial: OPT_BOOLEAN = Field(default=None)
    public_key: Annotated[
        Optional[CryptographicKey], BeforeValidator(get_value_from_array)
    ] = Field(default=None, **generate_aliases("publicKey", "security"))
    assertion_method: List[Multikey] = Field(
        default_factory=list, **generate_aliases("assertionMethod", "security")
    )


class Application(Actor):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Application",
        kw_only=True,
        alias="@type",
    )


class Group(Actor):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Group",
        kw_only=True,
        alias="@type",
    )


class Organization(Actor):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Organization",
        kw_only=True,
        alias="@type",
    )


class Person(Actor):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Person",
        kw_only=True,
        alias="@type",
    )


class Service(Actor):
    type: str = Field(
        default="https://www.w3.org/ns/activitystreams#Service",
        kw_only=True,
        alias="@type",
    )

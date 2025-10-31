from dataclasses import fields

from .context import LDContext
from .core import (
    Activity,
    Collection,
    CollectionPage,
    IntransitiveActivity,
    Link,
    Object,
    OrderedCollection,
    OrderedCollectionPage,
)
from .extra import Emoji, Hashtag
from .extra.cid import DataIntegrityProof, Multikey
from .extra.schema import PropertyValue
from .extra.security import CryptographicKey
from .nodeinfo import Nodeinfo
from .types import ActivityPubModel
from .vocab import (
    Application,
    Article,
    Audio,
    Document,
    Event,
    Group,
    Image,
    Mention,
    Note,
    Organization,
    Page,
    Person,
    Place,
    Profile,
    Service,
    Tombstone,
    Video,
)
from .vocab.activity import (
    Accept,
    Add,
    Announce,
    Arrive,
    Block,
    Create,
    Delete,
    Dislike,
    Flag,
    Follow,
    Ignore,
    Invite,
    Join,
    Leave,
    Like,
    Listen,
    Move,
    Offer,
    Question,
    Read,
    Reject,
    Remove,
    TentativeAccept,
    TentativeReject,
    Travel,
    Undo,
    Update,
    View,
)

_type_map = {
    # Core Types
    "Object": Object,
    "Link": Link,
    "Activity": Activity,
    "IntransitiveActivity": IntransitiveActivity,
    "Collection": Collection,
    "OrderedCollection": OrderedCollection,
    "CollectionPage": CollectionPage,
    "OrderedCollectionPage": OrderedCollectionPage,
    # Activity
    "Accept": Accept,
    "TentativeAccept": TentativeAccept,
    "Add": Add,
    "Announce": Announce,
    "Arrive": Arrive,
    "Block": Block,
    "Create": Create,
    "Delete": Delete,
    "Dislike": Dislike,
    "Flag": Flag,
    "Follow": Follow,
    "Ignore": Ignore,
    "Invite": Invite,
    "Join": Join,
    "Leave": Leave,
    "Like": Like,
    "Listen": Listen,
    "Move": Move,
    "Offer": Offer,
    "Question": Question,
    "Read": Read,
    "Reject": Reject,
    "TentativeReject": TentativeReject,
    "Remove": Remove,
    "Travel": Travel,
    "Undo": Undo,
    "Update": Update,
    "View": View,
    # Object Vocab
    "Person": Person,
    "Application": Application,
    "Group": Group,
    "Organization": Organization,
    "Service": Service,
    "Article": Article,
    "Document": Document,
    "Audio": Audio,
    "Image": Image,
    "Video": Video,
    "Page": Page,
    "Event": Event,
    "Place": Place,
    "Mention": Mention,
    "Note": Note,
    "Profile": Profile,
    "Tombstone": Tombstone,
    # CID
    "DataIntegrityProof": DataIntegrityProof,
    "Multikey": Multikey,
    # schema.org
    "PropertyValue": PropertyValue,
    # Others
    "Emoji": Emoji,
    "Hashtag": Hashtag,
}


def load(data: dict) -> dict | ActivityPubModel:
    if "type" in data and data["type"] in _type_map:
        cls = _type_map[data["type"]]
        kwargs = {}
        known_fields = {f.name for f in fields(cls)}
        for key, value in data.items():
            if key == "@context":
                kwargs["_context"] = LDContext(value)
            elif key in known_fields:
                if isinstance(value, dict):
                    kwargs[key] = load(value)
                elif isinstance(value, list):
                    kwargs[key] = [
                        load(v) if isinstance(v, dict) else v for v in value
                    ]
                else:
                    kwargs[key] = value
            else:
                kwargs.setdefault("_extra", {})[key] = value
        return cls(**kwargs)
    else:
        if Nodeinfo.is_nodeinfo_data(data):
            return Nodeinfo.from_json(data)
    return load_exact_match(data)


def load_exact_match(data: dict) -> dict | ActivityPubModel:
    if {"id", "owner", "publicKeyPem"} <= set(data.keys()):
        return CryptographicKey(**data)
    return data

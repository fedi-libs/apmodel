from typing import Annotated, List, Optional, Union  # noqa: F401

from pydantic import BeforeValidator, PlainSerializer  # noqa: F401

from ..core.activity import Activity
from ..core.collection import (
    Collection,
    CollectionPage,
    OrderedCollection,
    OrderedCollectionPage,
)

# ActivityStreams Vocab
from ..core.link import Link  # noqa: I001
from ..core.object import Object  # noqa: I001

# Extra models
from ..extra import Emoji, Hashtag  # noqa: F401
from ..extra.cid import DataIntegrityProof, Multikey  # noqa: F401
from ..extra.schema import PropertyValue  # noqa: F401
from ..extra.security import CryptographicKey  # noqa: F401
from ..helpers import (  # noqa: F401
    get_value_from_array,
    parse_ld_context,
    to_jld,
)

# Nodeinfo
from ..nodeinfo.nodeinfo import (
    Nodeinfo,  # noqa: F401
    NodeinfoInbound,  # noqa: F401
    NodeinfoOutbound,  # noqa: F401
    NodeinfoProtocol,  # noqa: F401
    NodeinfoServices,  # noqa: F401
    NodeinfoSoftware,  # noqa: F401
    NodeinfoUsage,  # noqa: F401
    NodeinfoUsageUsers,  # noqa: F401
)
from ..types import aliases  # noqa: F401
from ..types.aliases import (  # noqa: F401
    ID_OPT_STR,
    ID_OPT_STR_OR_OBJECT_OR_LINK,
    OPT_STR_OR_LINK,
    OPT_STR_OR_OBJECT_OR_LINK,
)
from ..vocab.activity.accept import Accept, TentativeAccept  # noqa: F401
from ..vocab.activity.add import Add  # noqa: F401
from ..vocab.activity.announce import Announce  # noqa: F401
from ..vocab.activity.arrive import Arrive  # noqa: F401
from ..vocab.activity.block import Block  # noqa: F401
from ..vocab.activity.create import Create  # noqa: F401
from ..vocab.activity.delete import Delete  # noqa: F401
from ..vocab.activity.dislike import Dislike  # noqa: F401
from ..vocab.activity.flag import Flag  # noqa: F401
from ..vocab.activity.follow import Follow  # noqa: F401
from ..vocab.activity.ignore import Ignore  # noqa: F401
from ..vocab.activity.invite import Invite  # noqa: F401
from ..vocab.activity.join import Join  # noqa: F401
from ..vocab.activity.leave import Leave  # noqa: F401
from ..vocab.activity.like import Like  # noqa: F401
from ..vocab.activity.listen import Listen  # noqa: F401
from ..vocab.activity.move import Move  # noqa: F401
from ..vocab.activity.offer import Offer  # noqa: F401
from ..vocab.activity.question import Question  # noqa: F401
from ..vocab.activity.read import Read  # noqa: F401
from ..vocab.activity.reject import Reject, TentativeReject  # noqa: F401
from ..vocab.activity.remove import Remove  # noqa: F401
from ..vocab.activity.travel import Travel  # noqa: F401
from ..vocab.activity.undo import Undo  # noqa: F401
from ..vocab.activity.update import Update  # noqa: F401
from ..vocab.activity.view import View  # noqa: F401
from ..vocab.actor import (  # noqa: F401
    Actor,
    Application,
    Group,
    Organization,
    Person,
    Service,
)
from ..vocab.article import Article  # noqa: F401
from ..vocab.document import Audio, Document, Image, Page, Video  # noqa: F401
from ..vocab.event import Event, Place  # noqa: F401
from ..vocab.mention import Mention  # noqa: F401
from ..vocab.note import Note  # noqa: F401
from ..vocab.profile import Profile  # noqa: F401
from ..vocab.tombstone import Tombstone  # noqa: F401

Object.model_rebuild()
Link.model_rebuild()
Activity.model_rebuild()
Collection.model_rebuild()
OrderedCollection.model_rebuild()
CollectionPage.model_rebuild()
OrderedCollectionPage.model_rebuild()
Actor.model_rebuild()
Person.model_rebuild()

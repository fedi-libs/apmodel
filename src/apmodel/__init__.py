from ._version import __version__, __version_tuple__  # noqa: F401

# from .dumper import dump
from .context import LDContext
from .core import (
    Activity,
    Collection,
    CollectionPage,
    IntransitiveActivity,  # noqa: F401
    Link,
    Object,
    OrderedCollection,
    OrderedCollectionPage,
)
from .loader import load
from .vocab import (
    Application,  # noqa: F401
    Group,  # noqa: F401
    Organization,  # noqa: F401
    Person,
    Service,  # noqa: F401
)

__all__ = [
    # Core Types
    "Object",
    "Link",
    "Activity",
    "Collection",
    "OrderedCollection",
    "CollectionPage",
    "OrderedCollectionPage",
    # Actor
    "Person",
    # load / dump
    "load",
    #    "dump",
    # context
    "LDContext",
]

Object.model_rebuild()
Link.model_rebuild()
Activity.model_rebuild()
Collection.model_rebuild()
OrderedCollection.model_rebuild()
CollectionPage.model_rebuild()
OrderedCollectionPage.model_rebuild()

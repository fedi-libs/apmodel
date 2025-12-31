from typing import Any

from apmodel.types import ActivityPubModel

from ._core._initial import _rebuild  # noqa: F401
from ._version import __version__, __version_tuple__  # noqa: F401
from .context import LDContext
from .core.activity import Activity
from .core.collection import (
    Collection,
    CollectionPage,
    OrderedCollection,
    OrderedCollectionPage,
)
from .loader import load
from .vocab.activity.announce import Announce
from .vocab.activity.create import Create
from .vocab.activity.delete import Delete
from .vocab.activity.follow import Follow
from .vocab.activity.undo import Undo
from .vocab.actor import Person
from .vocab.note import Note


def to_dict(obj: ActivityPubModel, **options) -> dict:
    raw_data = obj.model_dump(
        by_alias=True, exclude_none=True, **options
    )

    master_context = LDContext()

    def extract_and_clean(data: Any) -> Any:
        if isinstance(data, dict):
            new_dict = {}
            for k, v in data.items():
                if k == "@context":
                    master_context.add(v)
                else:
                    new_dict[k] = extract_and_clean(v)
            return new_dict

        elif isinstance(data, list):
            return [extract_and_clean(item) for item in data]

        return data

    if hasattr(obj, "_inference_context"):
        raw_data = obj._inference_context(raw_data)

    cleaned_result = extract_and_clean(raw_data)

    context_list = master_context.full_context
    if context_list:
        return {"@context": context_list, **cleaned_result}

    return cleaned_result


__all__ = [
    "Activity",
    "Announce",
    "Collection",
    "CollectionPage",
    "Create",
    "Delete",
    "Follow",
    "Note",
    "OrderedCollection",
    "OrderedCollectionPage",
    "Person",
    "Undo",
    "load",
    "to_dict",
]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types import ActivityPubModel

MODEL_DISPATCHER: dict[str, type["ActivityPubModel"]] = {}

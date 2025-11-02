from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from pydantic import Field

from ..vocab.actor import Actor
from .object import Object

if TYPE_CHECKING:
    from ..vocab.activity.accept import Accept
    from ..vocab.activity.reject import Reject
    from ..vocab.actor import Actor


class Activity(Object):
    type: Optional[str] = Field(default="Activity", kw_only=True)
    actor: Optional[Union[str, "Actor", List[Union[str, "Actor"]]]] = Field(
        default=None
    )
    object: Optional[Union[str, Object]] = Field(default=None)
    target: Optional[Union[str, "Actor", List[Union[str, "Actor"]]]] = Field(
        default=None
    )
    result: Optional[dict] = Field(default=None)
    origin: Optional[dict] = Field(default=None)
    instrument: Optional[dict] = Field(default=None)

    def accept(self, id: str, actor: Actor) -> "Accept":
        from ..vocab.activity.accept import Accept

        return Accept(id=id, object=self, actor=actor)

    def reject(self, id: str, actor: Actor) -> "Reject":
        from ..vocab.activity.reject import Reject

        return Reject(id=id, object=self, actor=actor)


@dataclass
class IntransitiveActivity(Activity):
    type: Union[str, Undefined] = Field(
        default="IntransitiveActivity", kw_only=True
    )

    def accept(self, id: str, actor: Actor) -> "Accept":
        from ..vocab.activity.accept import Accept

        return Accept(id=id, object=self, actor=actor)

    def reject(self, id: str, actor: Actor) -> "Reject":
        from ..vocab.activity.reject import Reject

        return Reject(id=id, object=self, actor=actor)

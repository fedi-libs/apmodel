from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from pydantic import ConfigDict, Field, ValidationInfo, field_validator
from pydantic.alias_generators import to_camel
from typing_extensions import Dict

from .object import Object

if TYPE_CHECKING:
    from ..vocab.activity.accept import Accept
    from ..vocab.activity.reject import Reject
    from ..vocab.actor import Actor


class Activity(Object):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        serialize_by_alias=True,
        extra="allow",
        revalidate_instances="never",
    )
    type: str = Field(default="Activity", kw_only=True, frozen=True)
    actor: Optional["str | Actor | List[str | Actor]"] = Field(default=None)
    object: Optional[str | Dict[str, Any] | Object] = Field(default=None)
    target: Optional["str | Actor | List[str | Actor]"] = Field(default=None)
    result: Optional[dict] = Field(default=None)
    origin: Optional[dict] = Field(default=None)
    instrument: Optional[dict] = Field(default=None)

    @field_validator("object", mode="before")
    @classmethod
    def convert_models(cls, v: Any, info: ValidationInfo) -> Any:
        from ..loader import load

        if isinstance(v, Object):
            return v
        if isinstance(v, str):
            return v
        if isinstance(v, dict):
            parent_context = info.data.get("context")
            if "@context" not in v and parent_context:
                v["@context"] = parent_context.full_context
            return load(v, "raw")
        return v

    def accept(self, id: str, actor: "Actor") -> "Accept":
        from ..vocab.activity.accept import Accept

        return Accept(id=id, object=self, actor=actor)

    def reject(self, id: str, actor: "Actor") -> "Reject":
        from ..vocab.activity.reject import Reject

        return Reject(id=id, object=self, actor=actor)


class IntransitiveActivity(Activity):
    type: str = Field(
        default="IntransitiveActivity", kw_only=True, frozen=True
    )

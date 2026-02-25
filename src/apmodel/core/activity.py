from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Union, Dict

import msgspec
from .object import Object

if TYPE_CHECKING:
    from ..vocab.activity.accept import Accept
    from ..vocab.activity.reject import Reject
    from ..vocab.actor import Actor


class Activity(Object):
    type: Optional[str] = msgspec.field(default="Activity")
    actor: Optional[Union[str, Actor, List[Union[str, Actor]]]] = msgspec.field(default=None)
    object: Optional[Union[str, Dict[str, Any], Object]] = msgspec.field(default=None)
    target: Optional[Union[str, Actor, List[Union[str, Actor]]]] = msgspec.field(default=None)
    result: Optional[dict] = msgspec.field(default=None)
    origin: Optional[dict] = msgspec.field(default=None)
    instrument: Optional[dict] = msgspec.field(default=None)

    @classmethod
    def model_validate(cls: type[Activity], data: Any, context: Optional[Dict[str, Any]] = None) -> Activity:
        if not isinstance(data, dict):
            if isinstance(data, cls):
                return data
            raise ValueError(f"Expected dict, got {type(data)}")

        ld_context = context.get("ld_context") if context else None
        
        # Pre-process fields that need conversion
        data_copy = data.copy()
        # Inherit fields from Object and add Activity's specific fields
        fields_to_validate = [
            "url", "attributedTo", "audience", "to", "bto", "cc", "bcc",
            "generator", "icon", "image", "inReplyTo", "location", "preview",
            "replies", "likes", "shares", "scope", "tag", "attachment",
            "actor", "object", "target"
        ]
        for field in fields_to_validate:
            if field in data_copy:
                data_copy[field] = cls._convert_field_to_model(data_copy[field], ld_context)
        
        return super(Object, cls).model_validate(data_copy, context=context)

    def accept(self, id: str, actor: "Actor") -> "Accept":
        from ..vocab.activity.accept import Accept

        return Accept(id=id, object=self, actor=actor)

    def reject(self, id: str, actor: "Actor") -> "Reject":
        from ..vocab.activity.reject import Reject

        return Reject(id=id, object=self, actor=actor)


class IntransitiveActivity(Activity):
    type: Optional[str] = msgspec.field(default="IntransitiveActivity")

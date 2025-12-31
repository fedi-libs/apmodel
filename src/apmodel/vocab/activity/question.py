import datetime
from typing import Any, Optional, cast

from pydantic import Field, field_serializer, field_validator
from typing_extensions import Dict

from ...core.activity import IntransitiveActivity
from ...core.link import Link
from ...core.object import Object
from ...types import ZDateTime


class Question(IntransitiveActivity):
    type: Optional[str] = Field(default="Question", kw_only=True, frozen=True)
    one_of: Optional[str | Object | Link | Dict[str, Any]] = Field(default=None)
    any_of: Optional[str | Object | Link | Dict[str, Any]] = Field(default=None)
    closed: Optional[
        str | Object | Link | Dict[str, Any] | ZDateTime | bool
    ] = Field(default=None)

    @field_validator("one_of", mode="before")
    @classmethod
    def validate_one_of(
        cls, v: Optional[str | Dict[str, Any]]
    ) -> Optional[str | Object | Link | Dict[str, Any]]:
        if not v:
            return None
        from ...loader import load

        return cast(Optional[str | Object | Link | Dict[str, Any]], load(v, "raw"))

    @field_validator("any_of", mode="before")
    @classmethod
    def validate_any_of(
        cls, v: Optional[str | Dict[str, Any]]
    ) -> Optional[str | Object | Link | Dict[str, Any]]:
        if not v:
            return None
        from ...loader import load

        return cast(Optional[str | Object | Link | Dict[str, Any]], load(v, "raw"))

    @field_validator("closed", mode="before")
    @classmethod
    def validate_closed(
        cls, v: Optional[str | Dict[str, Any]]
    ) -> Optional[str | Object | Link | Dict[str, Any]]:
        if not v:
            return None
        from ...loader import load

        return cast(Optional[str | Object | Link | Dict[str, Any]], load(v, "raw"))


        return value

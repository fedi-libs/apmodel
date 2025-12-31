import datetime
from typing import Any, Optional, cast

from pydantic import Field, field_serializer, field_validator
from typing_extensions import Dict

from ..core.object import Object
from ..types import ZDateTime

DeletedTypes = Optional[ZDateTime | str]


class Tombstone(Object):
    type: Optional[str] = Field(default="Tombstone", kw_only=True, frozen=True)
    former_type: Optional[str | Object | Dict[str, Any]] = Field(default=None)
    deleted: Optional[ZDateTime | str] = Field(default=None)

    @field_validator("former_type", mode="before")
    @classmethod
    def validate_former_type(
        cls, v: Optional[str | Dict[str, Any]]
    ) -> Optional[str | Object | Dict[str, Any]]:
        from ..loader import load

        if not v:
            return None
        return cast(Optional[str | Object | Dict[str, Any]], load(v, "raw"))

    @field_validator("deleted", mode="before")
    @classmethod
    def parse_deleted_datetime(cls, v: Any) -> DeletedTypes:
        if v is None or not isinstance(v, str):
            return v

        try:
            iso_string = v.replace("Z", "+00:00")
            return datetime.datetime.fromisoformat(iso_string)
        except ValueError as e:
            raise ValueError(
                f"Invalid ISO 8601 format for 'deleted' field: {v}. Error: {e}"
            )
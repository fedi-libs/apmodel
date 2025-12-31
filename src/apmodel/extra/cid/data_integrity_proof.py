from datetime import datetime, timezone
from typing import Optional

from pydantic import Field, field_serializer, field_validator

from ...context import LDContext
from ...types import ActivityPubModel, ZDateTime


class DataIntegrityProof(ActivityPubModel):
    context: LDContext = Field(
        default_factory=lambda: LDContext(
            [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/data-integrity/v1",
            ]
        ),
        kw_only=True,
        alias="@context",
    )

    type: Optional[str] = Field(default="DataIntegrityProof", kw_only=True)
    cryptosuite: str
    proof_value: str
    proof_purpose: str
    verification_method: str
    created: str | ZDateTime

    @field_validator("created", mode="before")
    @classmethod
    def convert_created_to_datetime(cls, v: str | datetime) -> datetime:
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        if isinstance(v, datetime):
            return v
        raise ValueError("created must be a string or a datetime object")
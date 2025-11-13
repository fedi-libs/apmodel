from typing import ClassVar

from pydantic import Field

from apmodel.helpers import generate_aliases
from apmodel.types.aliases import (
    JSONLD_CONTEXT,
    STR_OR_DATETIME,
    STRING,
)

from ...context import LDContext
from ...types import ActivityPubModel


class DataIntegrityProof(ActivityPubModel):
    context: JSONLD_CONTEXT = Field(
        default_factory=lambda: LDContext(
            [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/data-integrity/v1",
            ]
        ),
        alias="@context",
        kw_only=True, 
        exclude=True
    )
    AS_URI: ClassVar[str] = "https://w3id.org/security#DataIntegrityProof"

    cryptosuite: STRING = Field(**generate_aliases("cryptosuite", "security"))
    proof_value: STRING = Field(**generate_aliases("proofValue", "security"))
    proof_purpose: STRING = Field(**generate_aliases("proofPurpose", "security"))
    verification_method: STRING = Field(**generate_aliases("verificationMethod", "security"))
    created: STR_OR_DATETIME = Field(validation_alias="http://purl.org/dc/terms/created", serialization_alias="http://purl.org/dc/terms/created")
from pydantic import Field

from apmodel.types.aliases import (
    JSONLD_CONTEXT,
    OPT_STR,
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
    )

    type: str = Field(default="DataIntegrityProof", kw_only=True)
    cryptosuite: STRING
    proofValue: STRING
    proofPurpose: STRING
    verificationMethod: STRING
    created: STR_OR_DATETIME

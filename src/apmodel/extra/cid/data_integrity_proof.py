from datetime import datetime
from typing import Optional

import msgspec

from ...context import LDContext
from ...types import ActivityPubModel


class DataIntegrityProof(ActivityPubModel):
    cryptosuite: str
    proof_value: str
    proof_purpose: str
    verification_method: str
    created: datetime

    context: LDContext = msgspec.field(
        default_factory=lambda: LDContext(
            [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/data-integrity/v1",
            ]
        ),
        name="@context",
    )

    type: Optional[str] = msgspec.field(default="DataIntegrityProof")

from typing import ClassVar

from pydantic import ConfigDict, Field

from apmodel.helpers import generate_aliases
from apmodel.types.aliases import (
    PRIVKEY_MULTIBASE,
    PUBKEY_MULTIBASE,
    STRING,
)

from ...types import ActivityPubModel


class Multikey(ActivityPubModel):
    model_config = ConfigDict(
        serialize_by_alias=True,
        extra="allow",
        arbitrary_types_allowed=True
    )
    AS_URI: ClassVar[str] = "https://w3id.org/security#Multikey"

    id: str
    controller: STRING = Field(**generate_aliases("controller", "security"))

    public_key: PUBKEY_MULTIBASE = Field(
        default=None, **generate_aliases("publicKeyMultibase", "security")
    )
    secret_key: PRIVKEY_MULTIBASE = Field(
        default=None, **generate_aliases("secretKeyMultibase", "security")
    )
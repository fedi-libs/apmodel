from typing import Optional

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from multiformats import multibase, multicodec
from pydantic import Field, field_serializer

from apmodel.helpers import generate_aliases
from apmodel.types.aliases import (
    OPT_STR,
    PRIVKEY_MULTIBASE,
    PUBKEY_MULTIBASE,
    STRING,
)

from ...types import ActivityPubModel


class Multikey(ActivityPubModel):
    type: str = Field(
        alias="@type",
        default="https://w3id.org/security#Multikey",
        kw_only=True,
    )

    id: str
    controller: STRING = Field(**generate_aliases("controller", "security"))

    public_key: PUBKEY_MULTIBASE = Field(
        default=None, **generate_aliases("publicKeyMultibase", "security")
    )
    secret_key: PRIVKEY_MULTIBASE = Field(
        default=None, **generate_aliases("secretKeyMultibase", "security")
    )
    
    class Config:
        arbitrary_types_allowed = True
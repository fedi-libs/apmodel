from typing import Union

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from pydantic import Field, field_serializer

from apmodel.helpers import generate_aliases
from apmodel.types.aliases import PUBKEY_PEM, STRING

from ...types import ActivityPubModel


class CryptographicKey(ActivityPubModel):
    type: str = Field(
        default="https://w3id.org/security#publicKey",
        kw_only=True,
        alias="@type",
    )

    id: str = Field(validation_alias="@id", serialization_alias="@id")
    owner: STRING = Field(**generate_aliases("owner", "security"))
    public_key: PUBKEY_PEM = Field(**generate_aliases("publicKeyPem", "security"))

    class Config:
        arbitrary_types_allowed = True
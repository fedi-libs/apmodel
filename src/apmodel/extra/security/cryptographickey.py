from typing import ClassVar

from pydantic import ConfigDict, Field

from apmodel.helpers import generate_aliases
from apmodel.types.aliases import PUBKEY_PEM, STRING

from ...types import ActivityPubModel


class CryptographicKey(ActivityPubModel):
    model_config = ConfigDict(
        serialize_by_alias=True, extra="allow", arbitrary_types_allowed=True
    )
    AS_URI: ClassVar[str] = "https://w3id.org/security#Key"

    id: str = Field(validation_alias="@id", serialization_alias="@id")
    owner: STRING = Field(**generate_aliases("owner", "security"))
    public_key: PUBKEY_PEM = Field(
        **generate_aliases("publicKeyPem", "security")
    )
from typing import Optional

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pydantic import Field, PrivateAttr

from ...types import ActivityPubModel


class CryptographicKey(ActivityPubModel):
    type: str = Field(default="CryptographicKey", kw_only=True, frozen=True)

    id: str = Field()
    owner: Optional[str] = Field(default=None)
    public_key_pem: Optional[str | bytes] = Field(default=None)

    _public_key: Optional[rsa.RSAPublicKey] = PrivateAttr(None)

    @property
    def public_key(self) -> Optional[rsa.RSAPublicKey]:
        if not self.public_key_pem:
            return None
        elif isinstance(self.public_key_pem, str):
            k = self.public_key_pem.encode("utf-8")
        else:
            k = self.public_key_pem

        pub_key = serialization.load_pem_public_key(k)

        if isinstance(pub_key, rsa.RSAPublicKey):
            return pub_key
        else:
            raise ValueError(
                f"Unsupported Key Type: Expected RSAPublicKey, got {type(pub_key)}"
            )

    @public_key.setter
    def public_key(self, k: rsa.RSAPublicKey | rsa.RSAPrivateKey) -> None:
        if isinstance(k, rsa.RSAPrivateKey):
            k = k.public_key()

        self.public_key_pem = k.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

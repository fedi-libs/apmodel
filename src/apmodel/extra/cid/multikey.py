from typing import Optional

from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from pydantic import Field, PrivateAttr

from ..._core.key import (
    _encode_private_key_as_multibase,
    _encode_public_key_as_multibase,
    _load_private_key_from_multibase,
    _load_public_key_from_multibase,
)
from ...types import ActivityPubModel

PublicKeyTypes = str | ed25519.Ed25519PublicKey | rsa.RSAPublicKey
PrivateKeyTypes = str | ed25519.Ed25519PrivateKey | rsa.RSAPrivateKey


class Multikey(ActivityPubModel):
    type: Optional[str] = Field(default="Multikey", kw_only=True)

    id: str
    controller: str
    public_key_multibase: str | None = Field(default=None)
    secret_key_multibase: str | None = Field(default=None)

    _public_key: ed25519.Ed25519PublicKey | rsa.RSAPublicKey | None = PrivateAttr(None)
    _private_key: ed25519.Ed25519PrivateKey | rsa.RSAPrivateKey | None = PrivateAttr(
        None
    )

    @property
    def public_key(self):
        if self._public_key is None and self.public_key_multibase:
            self._public_key = _load_public_key_from_multibase(
                self.public_key_multibase
            )
        return self._public_key

    @property
    def private_key(self):
        if self._private_key is None and self.secret_key_multibase:
            self._private_key = _load_private_key_from_multibase(
                self.secret_key_multibase
            )
        return self._private_key

    @public_key.setter
    def public_key(
        self,
        key: ed25519.Ed25519PublicKey
        | rsa.RSAPublicKey
        | ed25519.Ed25519PrivateKey
        | rsa.RSAPrivateKey,
    ) -> None:
        if isinstance(key, ed25519.Ed25519PrivateKey) or isinstance(
            key, rsa.RSAPrivateKey
        ):
            key = key.public_key()
        self.public_key_multibase = _encode_public_key_as_multibase(key)

    @private_key.setter
    def private_key(
        self, key: ed25519.Ed25519PrivateKey | rsa.RSAPrivateKey
    ) -> None:
        self.secret_key_multibase = _encode_private_key_as_multibase(key)

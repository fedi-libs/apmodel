from typing import Optional

from cryptography.hazmat.primitives.asymmetric import ed25519, rsa

from ..._core.key import (
    _encode_private_key_as_multibase,
    _encode_public_key_as_multibase,
    _load_private_key_from_multibase,
    _load_public_key_from_multibase,
)
from ...types import ActivityPubModel
from ..utils.key import ActorKey

PublicKeyTypes = ed25519.Ed25519PublicKey | rsa.RSAPublicKey | None
PrivateKeyTypes = ed25519.Ed25519PrivateKey | rsa.RSAPrivateKey | None


class Multikey(ActivityPubModel):
    id: str
    controller: str

    type: str = "Multikey"
    public_key_multibase: Optional[str] = None
    secret_key_multibase: Optional[str] = None

    _public_key: PublicKeyTypes = None
    _private_key: PrivateKeyTypes = None

    @property
    def public_key(self) -> PublicKeyTypes:
        if self._public_key is None and self.public_key_multibase:
            self._public_key = _load_public_key_from_multibase(
                self.public_key_multibase
            )
        return self._public_key

    @property
    def private_key(self) -> PrivateKeyTypes:
        if self._private_key is None and self.secret_key_multibase:
            self._private_key = _load_private_key_from_multibase(
                self.secret_key_multibase
            )
        return self._private_key

    @public_key.setter
    def public_key(self, key: PublicKeyTypes | PrivateKeyTypes) -> None:
        if key:
            if isinstance(key, (ed25519.Ed25519PrivateKey, rsa.RSAPrivateKey)):
                key = key.public_key()
            self._public_key = key
            self.public_key_multibase = _encode_public_key_as_multibase(key)

    @private_key.setter
    def private_key(self, key: PrivateKeyTypes) -> None:
        if key:
            self._private_key = key
            self.secret_key_multibase = _encode_private_key_as_multibase(key)
            self.public_key = key.public_key()

    @property
    def as_key(self) -> ActorKey:
        if not self._private_key:
            raise ValueError("PrivateKey is not set.")
        return ActorKey(key_id=self.id, private_key=self._private_key)

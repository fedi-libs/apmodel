from typing import Optional, Union

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from ...types import ActivityPubModel
from ..utils.key import ActorKey


class CryptographicKey(ActivityPubModel, kw_only=True):
    id: str
    owner: Optional[str] = None
    public_key_pem: Optional[Union[str, bytes]] = None
    type: str = "CryptographicKey"

    _public_key: Optional[rsa.RSAPublicKey] = None
    _private_key: Optional[rsa.RSAPrivateKey] = None

    @property
    def public_key(self) -> Optional[rsa.RSAPublicKey]:
        if self._public_key is not None:
            return self._public_key

        if not self.public_key_pem:
            return None

        k = self.public_key_pem
        if isinstance(k, str):
            k = k.encode("utf-8")

        pub_key = serialization.load_pem_public_key(k)

        if isinstance(pub_key, rsa.RSAPublicKey):
            self._public_key = pub_key
            return pub_key
        else:
            raise ValueError(f"Unsupported Key Type: {type(pub_key)}")

    @public_key.setter
    def public_key(self, k: Union[rsa.RSAPublicKey, rsa.RSAPrivateKey]) -> None:
        if isinstance(k, rsa.RSAPrivateKey):
            self._private_key = k
            k = k.public_key()

        self._public_key = k
        self.public_key_pem = k.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

    @property
    def as_key(self) -> ActorKey:
        if not self._private_key:
            raise ValueError("PrivateKey is not set.")
        return ActorKey(key_id=self.id, private_key=self._private_key)

from typing import NamedTuple, Union

from cryptography.hazmat.primitives.asymmetric import ed25519, rsa

PrivateKeyTypes = Union[rsa.RSAPrivateKey, ed25519.Ed25519PrivateKey]


class ActorKey(NamedTuple):
    key_id: str
    private_key: PrivateKeyTypes

    @property
    def public_key(self):
        return self.private_key.public_key()

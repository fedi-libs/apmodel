from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from multiformats import multibase, multicodec


def _load_private_key_from_multibase(
    v: str,
) -> ed25519.Ed25519PrivateKey | rsa.RSAPrivateKey:
    try:
        decoded = multibase.decode(v)
        codec, data = multicodec.unwrap(decoded)

        if codec.name == "ed25519-priv":
            priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(data)
            return priv_key

        elif codec.name == "rsa-priv":
            priv_key = serialization.load_der_private_key(data, password=None)
            if not isinstance(priv_key, rsa.RSAPrivateKey):
                raise ValueError(f"Unsupported Key Type for rsa-priv: {type(priv_key)}")
            return priv_key

        else:
            raise ValueError(f"Unsupported Codec: {codec.name}")

    except Exception as e:
        raise ValueError(f"Invalid private key format or value: {e}")


def _load_public_key_from_multibase(
    v: str,
) -> ed25519.Ed25519PublicKey | rsa.RSAPublicKey:
    try:
        decoded = multibase.decode(v)
        codec, data = multicodec.unwrap(decoded)

        if codec.name == "ed25519-pub":
            pub_key = ed25519.Ed25519PublicKey.from_public_bytes(data)
            return pub_key

        elif codec.name == "rsa-pub":
            pub_key = serialization.load_der_public_key(data)
            if not isinstance(pub_key, rsa.RSAPublicKey):
                raise ValueError(f"Unsupported Key Type for rsa-pub: {type(pub_key)}")
            return pub_key

        else:
            raise ValueError(f"Unsupported Codec: {codec.name}")

    except Exception as e:
        raise ValueError(f"Invalid public key format or value: {e}")


def _encode_public_key_as_multibase(
    k: ed25519.Ed25519PublicKey | rsa.RSAPublicKey,
):
    if isinstance(k, rsa.RSAPublicKey):
        wrapped = multicodec.wrap(
            "rsa-pub",
            k.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.PKCS1,
            ),
        )
    elif isinstance(k, ed25519.Ed25519PublicKey):
        wrapped = multicodec.wrap(
            "ed25519-pub",
            k.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            ),
        )
    else:
        raise ValueError(f"Unsupported public key type: {type(k)}")
    return multibase.encode(wrapped, "base58btc")


def _encode_private_key_as_multibase(
    k: ed25519.Ed25519PrivateKey | rsa.RSAPrivateKey,
) -> str:
    if isinstance(k, rsa.RSAPrivateKey):
        wrapped = multicodec.wrap(
            "rsa-priv",
            k.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            ),
        )
    elif isinstance(k, ed25519.Ed25519PrivateKey):
        wrapped = multicodec.wrap(
            "ed25519-priv",
            k.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption(),
            ),
        )
    else:
        raise ValueError(f"Unsupported private key type: {type(k)}")
    return multibase.encode(wrapped, "base58btc")


__all__ = []

from datetime import datetime
from typing import Any, Dict, List, Literal, TypedDict, Union
from zoneinfo import ZoneInfo

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from multiformats import multibase, multicodec
from pydantic_core import PydanticCustomError

from apmodel.context import LDContext
from apmodel.exceptions import InvalidField


class GeneratedAliasesParams(TypedDict):
    validation_alias: str
    serialization_alias: str


def check_pem_type_by_header(pem_string: str) -> bool:
    cleaned_string = pem_string.replace("\r", "")
    first_line = cleaned_string.strip().split("\n")[0].strip()

    if "PRIVATE KEY" in first_line:
        return True
    elif "PUBLIC KEY" in first_line:
        return False
    else:
        raise ValueError("Unsupported PEM file")


def generate_aliases(
    suffix: str,
    schema: Literal[
        "as2", "schemaorg", "mastodon", "misskey", "security", "ldp"
    ] = "as2",
) -> GeneratedAliasesParams:
    """Generate arguments from schema name and suffix.

    Args:
        suffix (str): suffix
        schema (Literal["as2", "schemaorg", "mastodon", "misskey"]): The schema to which the suffix belongs

    Returns:
        dict: A dictionary containing arguments compatible with pydantic.
    """

    if schema == "as2":
        field_alias = f"https://www.w3.org/ns/activitystreams#{suffix}"
    elif schema == "misskey":
        field_alias = f"https://misskey-hub.net/ns#{suffix}"
    elif schema == "mastodon":
        field_alias = f"http://joinmastodon.org/ns#{suffix}"
    elif schema == "schemaorg":
        field_alias = f"http://schema.org#{suffix}"
    elif schema == "security":
        field_alias = f"https://w3id.org/security#{suffix}"
    elif schema == "ldp":
        field_alias = f"https://www.w3.org/ns/ldp#{suffix}"

    return {"validation_alias": field_alias, "serialization_alias": field_alias}


def has_match(data: Dict[str, Any], expected_keys: List[str]) -> bool:
    """
    Checks if all expected keys are present in the data dictionary.
    """
    return set(expected_keys).issubset(data.keys())


def get_value_from_array(v: Any) -> Any:
    """
    Pydantic validator to extract a single value from a JSON-LD property.
    It handles both single values and arrays. For arrays, it iterates
    and returns the first suitable value found.
    """
    if isinstance(v, list):
        for item in v:
            if isinstance(item, dict):
                if "@value" in item:
                    value = item["@value"]
                    value_type = item.get("@type")

                    if (
                        value_type
                        == "https://www.w3.org/2001/XMLSchema#dateTime"
                    ):
                        if isinstance(value, str):
                            dt_str = value
                            if dt_str.endswith("Z"):
                                dt_str = dt_str[:-1]
                            dt = datetime.fromisoformat(dt_str)
                            if dt.tzinfo is None:
                                dt = dt.replace(tzinfo=ZoneInfo("UTC"))
                            return dt
                    elif value_type == "https://w3id.org/security#multibase":
                        decoded = multibase.decode(value)
                        codec, data = multicodec.unwrap(decoded)
                        if codec.name == "ed25519-pub":
                            try:
                                pub_key = (
                                    ed25519.Ed25519PublicKey.from_public_bytes(
                                        data
                                    )
                                )
                                if isinstance(
                                    pub_key, ed25519.Ed25519PublicKey
                                ):
                                    return pub_key
                                else:
                                    raise ValueError(
                                        "Unsupported Key: {}".format(
                                            type(pub_key)
                                        )
                                    )
                            except InvalidKey:
                                raise InvalidField(
                                    "Invalid ed25519 public key passed."
                                )
                        elif codec.name == "rsa-pub":
                            try:
                                pub_key = serialization.load_der_public_key(
                                    data
                                )
                                if isinstance(pub_key, rsa.RSAPublicKey):
                                    return pub_key
                                else:
                                    raise ValueError(
                                        "Unsupported Key: {}".format(
                                            type(pub_key)
                                        )
                                    )
                            except ValueError:
                                raise InvalidField(
                                    "Invalid rsa public key passed."
                                )
                        elif codec.name == "ed25519-priv":
                            try:
                                priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(
                                    data
                                )
                                if isinstance(
                                    priv_key, ed25519.Ed25519PrivateKey
                                ):
                                    return priv_key
                                else:
                                    raise ValueError(
                                        "Unsupported Key: {}".format(
                                            type(priv_key)
                                        )
                                    )
                            except InvalidKey:
                                raise InvalidField(
                                    "Invalid ed25519 private key passed."
                                )
                        elif codec.name == "rsa-priv":
                            try:
                                priv_key = serialization.load_der_private_key(
                                    data, password=None
                                )
                                if isinstance(priv_key, rsa.RSAPrivateKey):
                                    return priv_key
                                else:
                                    raise ValueError(
                                        "Unsupported Key: {}".format(
                                            type(priv_key)
                                        )
                                    )
                            except ValueError:
                                raise InvalidField(
                                    "Invalid rsa private key passed."
                                )
                        else:
                            raise ValueError(
                                "Unsupported Codec: {}".format(codec.name)
                            )
                    return value
                elif "@id" in item:
                    value = item["@id"]
                    return value
            else:
                return item
    return v


def parse_ld_context(v: List) -> LDContext:
    if not isinstance(v, list):
        raise PydanticCustomError(
            "invalid_type",
            "Input must be a list to be converted to LDContexts, got {input_type}",
            {"input_type": type(v).__name__},
        )

    return LDContext(v)


def load_pem_key(
    v: Union[
        str,
        rsa.RSAPublicKey,
        rsa.RSAPrivateKey,
        ed25519.Ed25519PrivateKey,
        ed25519.Ed25519PublicKey,
    ],
    private: bool = False,
) -> Union[
    rsa.RSAPublicKey,
    rsa.RSAPrivateKey,
    ed25519.Ed25519PrivateKey,
    ed25519.Ed25519PublicKey,
]:
    if not isinstance(v, str):
        return v
    if private:
        key = serialization.load_pem_private_key(
            v.encode("utf-8"), password=None
        )
        if not isinstance(key, (rsa.RSAPrivateKey, ed25519.Ed25519PrivateKey)):
            raise InvalidField("Unsupported private key passed.")
        return key
    else:
        key = serialization.load_pem_public_key(v.encode("utf-8"))
        if not isinstance(key, (rsa.RSAPublicKey, ed25519.Ed25519PublicKey)):
            raise InvalidField("Unsupported public key passed.")
        return key


def ser_multibase(
    v: Union[
        rsa.RSAPublicKey,
        ed25519.Ed25519PublicKey,
        rsa.RSAPrivateKey,
        ed25519.Ed25519PrivateKey,
    ],
) -> str:
    if isinstance(v, rsa.RSAPrivateKey):
        wrapped = multicodec.wrap(
            "rsa-priv",
            v.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            ),
        )
    elif isinstance(v, ed25519.Ed25519PrivateKey):
        wrapped = multicodec.wrap(
            "ed25519-priv",
            v.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption(),
            ),
        )
    elif isinstance(v, rsa.RSAPublicKey):
        wrapped = multicodec.wrap(
            "rsa-pub",
            v.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.PKCS1,
            ),
        )
    elif isinstance(v, ed25519.Ed25519PublicKey):
        wrapped = multicodec.wrap(
            "ed25519-pub",
            v.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            ),
        )
    return multibase.encode(wrapped, "base58btc")


def ser_public_key_pem(
    v: Union[rsa.RSAPublicKey, ed25519.Ed25519PublicKey],
) -> str:
    if isinstance(v, rsa.RSAPublicKey):
        return v.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
    elif isinstance(v, ed25519.Ed25519PublicKey):
        return v.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Optional, TypeAlias, Union

from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from pydantic import BeforeValidator, PlainSerializer

from ..context import LDContext
from ..helpers import (
    get_value_from_array,
    load_pem_key,
    parse_ld_context,
    ser_public_key_pem,
    to_jld,
)

if TYPE_CHECKING:
    from ..core.link import Link
    from ..core.object import Object


JSONLD_CONTEXT: TypeAlias = Annotated[
    LDContext, BeforeValidator(parse_ld_context)
]

OPT_STR: TypeAlias = Annotated[
    Optional[str],
    BeforeValidator(get_value_from_array),
    PlainSerializer(to_jld()),
]

OPT_STR_OR_LINK: TypeAlias = Annotated[
    Optional[Union[str, "Link"]],
    BeforeValidator(get_value_from_array),
    PlainSerializer(to_jld()),
]

OPT_STR_OR_OBJECT_OR_LINK: TypeAlias = Annotated[
    Optional[Union[str, "Object", "Link"]],
    BeforeValidator(get_value_from_array),
    PlainSerializer(to_jld()),
]

OPT_DATETIME: TypeAlias = Annotated[
    Optional[datetime],
    BeforeValidator(get_value_from_array),
    PlainSerializer(to_jld()),
]

OPT_STR_OR_DATETIME: TypeAlias = Annotated[
    Optional[Union[str, datetime]],
    BeforeValidator(get_value_from_array),
    PlainSerializer(to_jld()),
]

ID_OPT_STR_OR_OBJECT_OR_LINK: TypeAlias = Annotated[
    Optional[Union[str, "Object", "Link"]],
    BeforeValidator(get_value_from_array),
]

ID_OPT_STR: TypeAlias = Annotated[
    Optional[str], BeforeValidator(get_value_from_array)
]

STR_OR_DATETIME: TypeAlias = Annotated[
    Union[str, datetime],
    BeforeValidator(get_value_from_array),
    PlainSerializer(to_jld()),
]
OPT_BOOLEAN: TypeAlias = Annotated[
    Optional[bool],
    BeforeValidator(get_value_from_array),
    PlainSerializer(to_jld()),
]
OPT_FLOAT: TypeAlias = Annotated[
    Optional[float],
    BeforeValidator(get_value_from_array),
    PlainSerializer(to_jld()),
]

STRING: TypeAlias = Annotated[str, BeforeValidator(get_value_from_array)]
BOOLEAN: TypeAlias = Annotated[bool, BeforeValidator(get_value_from_array)]
FLOAT: TypeAlias = Annotated[float, BeforeValidator(get_value_from_array)]

PUBKEY_MULTIBASE: TypeAlias = Annotated[
    Optional[Union[rsa.RSAPublicKey, ed25519.Ed25519PublicKey]],
    BeforeValidator(get_value_from_array),
    PlainSerializer(to_jld()),
]
PRIVKEY_MULTIBASE: TypeAlias = Annotated[
    Optional[Union[rsa.RSAPrivateKey, ed25519.Ed25519PrivateKey]],
    BeforeValidator(get_value_from_array),
    PlainSerializer(to_jld()),  # ser_multibase
]
PUBKEY_PEM: TypeAlias = Annotated[
    Optional[Union[rsa.RSAPublicKey, ed25519.Ed25519PublicKey]],
    BeforeValidator(lambda v: load_pem_key(v, False)),
    PlainSerializer(ser_public_key_pem),
]

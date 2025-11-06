import datetime
from typing import Annotated, ClassVar, Optional, TypeAlias, Union

from pydantic import BeforeValidator, Field

from apmodel.helpers import generate_aliases, get_value_from_array

from ...core.activity import IntransitiveActivity
from ...core.link import Link
from ...core.object import Object

OPT_ID_OR_OBJ_OR_LINK: TypeAlias = Annotated[
    Optional[Union[str, Object, Link]], BeforeValidator(get_value_from_array)
]


class Question(IntransitiveActivity):
    AS_URI: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Question"

    one_of: OPT_ID_OR_OBJ_OR_LINK = Field(default=None, **generate_aliases("oneOf", "as2"))
    any_of: OPT_ID_OR_OBJ_OR_LINK = Field(default=None, **generate_aliases("anyOf", "as2"))
    closed: Annotated[
        Optional[Union[str, Object, Link, datetime.datetime, bool]],
        BeforeValidator(get_value_from_array),
    ] = Field(default=None, **generate_aliases("closed", "as2"))
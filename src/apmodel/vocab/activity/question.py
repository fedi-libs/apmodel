import datetime
from typing import Annotated, Optional, TypeAlias, Union

from pydantic import BeforeValidator, Field

from apmodel.helpers import get_value_from_array

from ...core.activity import IntransitiveActivity
from ...core.link import Link
from ...core.object import Object

OPT_ID_OR_OBJ_OR_LINK: TypeAlias = Annotated[
    Optional[Union[str, Object, Link]], BeforeValidator(get_value_from_array)
]


class Question(IntransitiveActivity):
    type: str = Field(
        alias="@type",
        default="https://www.w3.org/ns/activitystreams#Question",
        kw_only=True,
    )
    oneOf: OPT_ID_OR_OBJ_OR_LINK = Field(default=None)
    anyOf: OPT_ID_OR_OBJ_OR_LINK = Field(default=None)
    closed: Annotated[
        Optional[Union[str, Object, Link, datetime.datetime, bool]],
        BeforeValidator(get_value_from_array),
    ] = Field(default=None)
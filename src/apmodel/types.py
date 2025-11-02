from typing import Annotated, Any, Dict, List, Optional

from pydantic import BaseModel, BeforeValidator, Field, model_validator
from pydantic_core import PydanticCustomError

from .context import LDContext


def parse_ld_context(v: List) -> LDContext:
    if not isinstance(v, list):
        raise PydanticCustomError(
            "invalid_type",
            "Input must be a list to be converted to LDContexts, got {input_type}",
            {"input_type": type(v).__name__},
        )

    return LDContext(v)


class ActivityPubModel(BaseModel):
    context: Annotated[LDContext, BeforeValidator(parse_ld_context)] = Field(
        alias="@context"
    )

    @model_validator(mode="before")
    @classmethod
    def save_raw_data(cls, data: Any) -> Any:
        if isinstance(data, dict):
            data["_raw_data_internal_key"] = data.copy()
        return data

    @property
    def _raw_json(self) -> Optional[Dict[str, Any]]:
        return self.__dict__.get("_raw_data_internal_key")

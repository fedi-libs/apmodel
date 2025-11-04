from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, model_validator

from apmodel.types.aliases import JSONLD_CONTEXT


class ActivityPubModel(BaseModel):
    context: JSONLD_CONTEXT = Field(alias="@context")

    @model_validator(mode="before")
    @classmethod
    def save_raw_data(cls, data: Any) -> Any:
        if isinstance(data, dict):
            data["_raw_data_internal_key"] = data.copy()
        return data

    @property
    def _raw_json(self) -> Optional[Dict[str, Any]]:
        return self.__dict__.get("_raw_data_internal_key")

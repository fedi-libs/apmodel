import warnings
from typing import Any, ClassVar, Dict, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)
from pyld.context_resolver import jsonld

from apmodel.types.aliases import JSONLD_CONTEXT

from .._initial._dispatch import MODEL_DISPATCHER


class ActivityPubModel(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True, extra="allow")
    AS_URI: ClassVar[str] = "__apmodel_base__"

    context: JSONLD_CONTEXT = Field(alias="@context")
    type: Optional[str] = Field(
        alias="@type", default=None, kw_only=True, frozen=True
    )

    raw_data_internal_key: Optional[Dict[str, Any]] = Field(
        default=None, exclude=True
    )

    @model_validator(mode="after")
    def set_type_after_validation(self) -> "ActivityPubModel":
        if self.type is None:
            object.__setattr__(self, "type", self.AS_URI)
        return self

    @model_validator(mode="before")
    @classmethod
    def save_raw_data(cls, data: Any) -> Any:
        if isinstance(data, dict):
            data["raw_data_internal_key"] = data.copy()
        return data

    @property
    def _raw_json(self) -> Optional[Dict[str, Any]]:
        return self.raw_data_internal_key

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        model_type = cls.AS_URI

        if not model_type or model_type == "__apmodel_base__":
            return

        if model_type in MODEL_DISPATCHER:
            existing_cls = MODEL_DISPATCHER[model_type]
            from apmodel.core.activity import Activity, IntransitiveActivity
            from apmodel.core.collection import (
                Collection,
                CollectionPage,
                OrderedCollection,
                OrderedCollectionPage,
            )
            from apmodel.core.link import Link
            from apmodel.core.object import Object

            if issubclass(cls, existing_cls) and existing_cls not in [
                Object,
                Link,
                Activity,
                Collection,
                CollectionPage,
                OrderedCollection,
                OrderedCollectionPage,
                IntransitiveActivity,
            ]:  # cls can't override if existing_cls is in base models
                MODEL_DISPATCHER[model_type] = cls
                return
            else:
                warnings.warn(
                    f"Model type '{model_type}' for class {cls.__name__} conflicts with "
                    f"existing model {existing_cls.__name__}. Registration skipped due to "
                    f"missing inheritance relationship (Must inherit from {existing_cls.__name__}).",
                    UserWarning,
                    stacklevel=2,
                )
                return

        if isinstance(model_type, str):
            MODEL_DISPATCHER[model_type] = cls

    def dump(self, compact: bool = True, **kwargs):
        """Dump the model.
        
        Dump model to jsonld-compatible dictionary.
        
        Args:
            compact (boolean): If set True, apmodel run jsonld.compact in function and return compacted json-ld data.
            **kwargs (any): extra arguments pass to pydantic's model_dump function.
        
        Returns:
            dict: exported model dict.
        """
        d = self.model_dump(**kwargs)
        if compact:
            d = jsonld.compact(d, d["@context"])
        return d

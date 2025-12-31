import datetime
from typing import Annotated, Any, Dict, Optional, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    model_serializer,
    model_validator,
)
from pydantic.alias_generators import to_camel
from pydantic.functional_serializers import PlainSerializer
from typing_extensions import TypeAlias

from .context import LDContext

T = TypeVar("T", bound="ActivityPubModel")
ZDateTime: TypeAlias = Annotated[
    datetime.datetime,
    PlainSerializer(
        lambda v: (
            v if v.tzinfo else v.replace(tzinfo=datetime.timezone.utc)
        ).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ").replace(".000000Z", "Z")
    ),
]


class ActivityPubModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        serialize_by_alias=True,
        extra="allow",
        revalidate_instances="never",
    )

    def __post_init__(self):
        if hasattr(self, "context"):
            self.context = LDContext(self.context)

    @model_validator(mode="before")
    @classmethod
    def validate_secret(cls, d: Any) -> LDContext | Any:
        if hasattr(cls, "context"):
            return LDContext(d)
        return d

    def dump(self, **kwargs) -> dict:
        out = super().model_dump(exclude_none=True, **kwargs)
        return out

    @model_serializer(when_used="json")
    def serialize_to_json_ld(self) -> Dict[str, Any]:
        aggregated_context: Optional[LDContext]
        try:
            aggregated_context = self.context + LDContext()
        except AttributeError:
            aggregated_context = None

        data: Dict[str, Any] = {}

        for field_name, field_info in self.__class__.model_fields.items():
            value = getattr(self, field_name)

            if field_name.startswith("_") or not value:
                continue

            if isinstance(value, ActivityPubModel):
                child_json = value.serialize_to_json_ld()

                if aggregated_context:
                    if hasattr(value, "context") and value.context:
                        aggregated_context = aggregated_context + value.context

                    child_json.pop("@context", None)
                data[field_name] = child_json

            elif isinstance(value, list):
                processed_list = []
                for item in value:
                    if isinstance(item, ActivityPubModel):
                        child_json = item.serialize_to_json_ld()

                        if aggregated_context:
                            if hasattr(item, "context") and item.context:
                                aggregated_context = (
                                    aggregated_context + item.context
                                )
                            child_json.pop("@context", None)
                        processed_list.append(child_json)
                    else:
                        processed_list.append(item)
                data[field_name] = processed_list

            else:
                data[field_name] = value

        if aggregated_context:
            data["@context"] = aggregated_context.full_context

        return data

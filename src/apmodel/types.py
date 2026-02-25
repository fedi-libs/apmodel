import datetime
from typing import Annotated, Any, Dict, Optional, TypeVar, List, Union
import msgspec
from typing_extensions import TypeAlias

from .context import LDContext

T = TypeVar("T", bound="ActivityPubModel")

def _format_datetime(v: datetime.datetime) -> str:
    if v.tzinfo is None:
        v = v.replace(tzinfo=datetime.timezone.utc)
    return v.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ").replace(".000000Z", "Z")

ZDateTime: TypeAlias = Annotated[
    datetime.datetime,
    msgspec.field(name="dateTime") # This is just a placeholder, msgspec handles datetime
]

class BaseModel(msgspec.Struct, rename="camel", omit_defaults=True):
    @classmethod
    def model_validate(cls: type[T], data: Any) -> T:
        if isinstance(data, cls):
            return data
        try:
            return msgspec.convert(data, cls, strict=False)
        except Exception as e:
            raise ValueError(f"Validation failed for {cls.__name__}: {e}") from e

    def model_dump(self, mode: str = "json", **kwargs) -> Dict[str, Any]:
        if mode == "json":
            encoded = msgspec.json.encode(self)
            return msgspec.json.decode(encoded)
        return msgspec.to_builtins(self)

class ActivityPubModel(BaseModel, dict=True):
    # We use dict=True to allow model_extra-like behavior and __dict__ access

    @property
    def model_extra(self) -> Dict[str, Any]:
        if not hasattr(self, "_model_extra"):
            self._model_extra = {}
        return self._model_extra

    def __post_init__(self):
        if hasattr(self, "context"):
            self.context = LDContext(self.context)

    @classmethod
    def model_validate(cls: type[T], data: Any, context: Optional[Dict[str, Any]] = None) -> T:
        if not isinstance(data, dict):
            if isinstance(data, cls):
                return data
            raise ValueError(f"Expected dict, got {type(data)}")

        # For ActivityPubModel, we need to handle extra fields
        field_info = msgspec.structs.fields(cls)
        encoded_to_python = {
            (f.encode_name if f.encode_name is not None else f.name): f.name
            for f in field_info
        }

        extra_data = {}
        for k, v in data.items():
            if k not in encoded_to_python:
                extra_data[k] = v

        try:
            instance = msgspec.convert(data, cls, strict=False)
            instance._model_extra = extra_data
            
            if hasattr(instance, "__post_init__"):
                instance.__post_init__()
                
            return instance
        except Exception as e:
            raise ValueError(f"Validation failed for {cls.__name__}: {e}") from e

    def model_dump(self, mode: str = "python", **kwargs) -> Dict[str, Any]:
        # Mimic Pydantic's model_dump
        # mode="json" should return camelCase
        # mode="python" should return snake_case (Pydantic default)
        
        # Actually, apmodel uses model_dump(exclude_none=True) and expects camelCase 
        # because of serialize_by_alias=True in Pydantic config.
        
        data = msgspec.to_builtins(self)
        
        if mode == "json":
            # msgspec.to_builtins returns Python names by default.
            # To get renamed keys, we can use a trick:
            encoded = msgspec.json.encode(self)
            data = msgspec.json.decode(encoded)
        
        # Merge model_extra
        if hasattr(self, "_model_extra"):
            data.update(self._model_extra)
            
        return data

    def dump(self, **kwargs) -> dict:
        return self.model_dump(mode="json", **kwargs)

    def serialize_to_json_ld(self) -> Dict[str, Any]:
        aggregated_context: Optional[LDContext]
        try:
            aggregated_context = self.context + LDContext()
        except AttributeError:
            aggregated_context = None

        data: Dict[str, Any] = {}

        # Use msgspec to get fields
        for f in msgspec.structs.fields(self.__class__):
            field_name = f.name
            encoded_name = f.encode_name if f.encode_name is not None else field_name
            value = getattr(self, field_name)

            if field_name.startswith("_") or value is None:
                continue
                
            # Handle empty lists/dicts if needed? Pydantic was "not value"
            if not value and not isinstance(value, (bool, int, float)):
                continue

            if isinstance(value, ActivityPubModel):
                child_json = value.serialize_to_json_ld()

                if aggregated_context:
                    if hasattr(value, "context") and value.context:
                        aggregated_context = aggregated_context + value.context

                    child_json.pop("@context", None)
                data[encoded_name] = child_json

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
                data[encoded_name] = processed_list

            else:
                # Handle datetime serialization specifically if it's a ZDateTime
                if isinstance(value, datetime.datetime):
                    data[encoded_name] = _format_datetime(value)
                else:
                    data[encoded_name] = value

        # Merge extra fields
        if hasattr(self, "_model_extra"):
            for k, v in self._model_extra.items():
                data[k] = v

        if aggregated_context:
            data["@context"] = aggregated_context.full_context

        return data

    @classmethod
    def model_rebuild(cls, **kwargs):
        # Pydantic v2 has this, msgspec doesn't need it but we keep it for compatibility if called
        pass

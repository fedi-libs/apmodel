from datetime import datetime
from typing import Any, Dict, List
from zoneinfo import ZoneInfo


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
    items = v if isinstance(v, list) else [v]

    for item in items:
        if isinstance(item, dict):
            if "@value" in item:
                value = item["@value"]
                value_type = item.get("@type")

                if value_type == "https://www.w3.org/2001/XMLSchema#dateTime":
                    if isinstance(value, str):
                        dt_str = value
                        if dt_str.endswith("Z"):
                            dt_str = dt_str[:-1]
                        dt = datetime.fromisoformat(dt_str)
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
                        return dt
                return value
        else:
            return item

    return None

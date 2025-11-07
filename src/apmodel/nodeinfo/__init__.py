from .nodeinfo import Nodeinfo

def load(data: dict) -> Nodeinfo:
    return Nodeinfo.model_validate(data)
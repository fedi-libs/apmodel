from pyld import jsonld

from ._initial._dispatch import MODEL_DISPATCHER


def get_avaliable_models():
    return MODEL_DISPATCHER


def load(data: dict):
    expanded = jsonld.expand(data)[0]
    
    if expanded == []:
        return data
        
    dict_type = expanded.get("@type")

    if isinstance(dict_type, list):
        dict_type = dict_type[0]

    if not dict_type:
        return data

    m = MODEL_DISPATCHER.get(dict_type)

    if not m:
        return data

    loaded_data = m.model_validate(data)
    return loaded_data

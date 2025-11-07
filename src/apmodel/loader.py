from pyld import jsonld

from ._initial._dispatch import MODEL_DISPATCHER


def get_avaliable_models():
    return MODEL_DISPATCHER


def load(data: dict):
    expanded = jsonld.expand(data)
    
    if expanded == []:
        return data
        
    dict_type = expanded[0].get("@type")

    if isinstance(dict_type, list):
        dict_type = dict_type[0]

    if not dict_type:
        return data

    m = MODEL_DISPATCHER.get(dict_type)

    if not m:
        return data

    loaded_data = m.model_validate(data)
    if "type" in data and dict_type:
        data_copy = data.copy()
        del data_copy["type"]
        loaded_data = m.model_validate(data_copy)
    else:
        loaded_data = m.model_validate(data)
    return loaded_data

from pyld import jsonld

from ._initial._dispatch import MODEL_DISPATCHER


def get_avaliable_models():
    return MODEL_DISPATCHER


def load(data: dict):
    expanded = jsonld.expand(data)

    if not expanded:
        return data

    dict_type_val = expanded[0].get("@type")

    if isinstance(dict_type_val, list):
        dict_type = dict_type_val[0]
    else:
        dict_type = dict_type_val

    if not dict_type:
        return data

    m = MODEL_DISPATCHER.get(dict_type)

    if not m:
        return data

    data_for_validation = data.copy()
    if "type" in data_for_validation and dict_type:
        del data_for_validation["type"]

    data_for_validation["__APMODEL_TOP_LEVEL__"] = True
    loaded_data = m.model_validate(data_for_validation)

    return loaded_data

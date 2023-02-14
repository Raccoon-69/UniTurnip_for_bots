import json


# ================================================================
# ===========================| Tools |============================
# ================================================================
def read_schema(string: str | dict):
    if type(string) == str:
        if "'" in string:
            string = string.replace("'", '"')
        return json.loads(string)
    elif type(string) == dict:
        return string
    else:
        raise TypeError(type(string))


# ----------------------------------------------------------------
def schema_error_check(schema: dict):
    if 'required' not in schema.keys() or 'properties' not in schema.keys():
        raise KeyError('The schema must have keys "required" and "properties"')
    for property in schema['properties'].values():
        if 'type' not in property or 'title' not in property:
            raise KeyError(f'Keys "type" and "title" where not found in property keys ({property.keys()}')


# ----------------------------------------------------------------
def merge_dict(dict1, dict2):
    if dict1 and dict2:
        dict1.update(dict2)
        return dict1
    elif dict1 is None and dict2:
        return dict2
    elif dict2 is None and dict1:
        return dict1
    else:
        return None

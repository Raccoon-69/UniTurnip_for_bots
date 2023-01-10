import json


def read_schema(string: str | dict):
    if type(string) == str:
        if "'" in string:
            string = string.replace("'", '"')
        return json.loads(string)
    elif type(string) == dict:
        return string
    else:
        raise TypeError(type(string))


def schema_error_check(schema: dict):
    if 'required' not in schema.keys() or 'properties' not in schema.keys():
        raise KeyError('The schema must have keys "required" and "properties"')
    for property in schema['properties'].values():
        if 'type' not in property or 'title' not in property:
            raise KeyError(f'Keys "type" and "title" where not found in property keys ({property.keys()}')



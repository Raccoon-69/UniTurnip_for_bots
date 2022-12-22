import json


def read_schema(demo_schema: str | dict):
    if type(demo_schema) == str:
        schema = str_to_dict(demo_schema)
    elif type(demo_schema) == dict:
        schema = demo_schema
    else:
        raise TypeError
    schema_error_check(schema)
    return schema


def str_to_dict(string):
    if type(string) == str:
        if "'" in string:
            string = string.replace("'", '"')
        return json.loads(string)
    elif type(string) == dict:
        return string
    else:
        raise TypeError(type(string))


def schema_error_check(schema):
    if 'required' not in schema.keys() or 'properties' not in schema.keys():
        raise KeyError('The schema must have keys "required" and "properties"')
    for property in schema['properties'].values():
        if 'type' not in property or 'title' not in property:
            raise KeyError(f'Keys "type" and "title" where not found in property keys ({property.keys()}')



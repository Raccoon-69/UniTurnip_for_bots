from UniTurnip_for_bots.handlers.inline_keyboards import create_custom_keyboards


class SchemaRead:
    def __init__(self, schema):
        self.questions_list = []
        self.last_type = None
        self.required = []
        self.last_key = None
        self.schema = schema
        self.schema_read(schema)
        self.stencil = self.response_stencil(schema)

    def get(self):
        return self.questions_list, self.stencil

    # ===================================================================================
    # ================================| read_the_schema |================================
    # ===================================================================================
    def schema_read(self, schema):
        if 'type' in schema.keys() and not self.last_type:
            self.last_type = schema['type']
        if 'required' in schema.keys():
            self.required = schema['required']
        for key, value in schema.items():
            if type(value) == dict:
                if 'type' in value.keys():
                    if value['type'] == 'array':
                        self.last_key = key
                    if value['type'] in ('string', 'boolean', 'number', 'integer'):
                        self.questions_creating(key, value)
                    else:
                        if 'type' in schema.keys():
                            self.last_type = schema['type']
                        self.schema_read(value)
                else:
                    self.schema_read(value)
            elif type(value) == list:
                pass
            elif type(value) == str:
                pass
        self.last_key = None

    def questions_creating(self, param_key, schema):

        def required_keys(param_key_, schema_):
            if 'type' in schema_.keys() and 'title' in schema_.keys():
                question = {'type': schema_['type'], 'question': schema_['title']}
            else:
                return False
            if 'enum' in schema.keys():
                question['enum'] = schema['enum']
            question['required'] = True if param_key_ in self.required else False
            question['last_type'] = self.last_type
            question['keyboard'], question['keyboard_settings'] = create_custom_keyboards(question)
            return question

        if question := required_keys(param_key, schema):

            question['answer_settings'] = {}
            if 'minLength' in schema.keys():
                question['answer_settings']['minLength'] = schema['minLength']
            if 'minimum' in schema.keys():
                question['answer_settings']['minimum'] = schema['minimum']
            if 'maximum' in schema.keys():
                question['answer_settings']['maximum'] = schema['maximum']
            if 'multipleOf' in schema.keys():
                question['answer_settings']['multipleOf'] = schema['multipleOf']
            if 'description' in schema.keys():
                question['question'] += f'\n{schema["description"]}'

            if self.last_type == 'array':
                end_questions = required_keys('UniTurnipMore', {'title': 'Еще?', 'type': 'more_q'})
                if 'type' not in self.questions_list[-1][1]:
                    dict_with_questions = self.questions_list[-1][1]
                    key = max(dict_with_questions.keys())
                    dict_with_questions[key] = (param_key, question)
                    dict_with_questions[key+1] = ('UniTurnipMore', end_questions)
                    self.questions_list[-1] = (self.last_key, dict_with_questions)
                else:
                    dict_with_questions = {0: (param_key, question), 1: ('UniTurnip', end_questions)}
                    self.questions_list += [(self.last_key, dict_with_questions)]
                return
            self.questions_list += [(param_key, question)]

    # ======================================================================================
    # ================================| create the stencil |================================
    # ======================================================================================
    def response_stencil(self, schema, ref=None):
        if ref:
            return self.unpacking_a_dictionary_with_different_questions(schema, ref['properties'].items())
        if type(schema) == dict:
            if 'type' in schema:
                if 'properties' in schema.keys():
                    properties = schema['properties'].items()
                elif 'items' in schema.keys():
                    if type(schema['items']) == dict:
                        if '$ref' in schema['items'].keys():
                            ref = schema['items']['$ref']
                            return self.response_stencil(schema, ref=self.open_ref(ref, self.schema))
                        elif schema['items']['type'] == 'object':
                            properties = schema['items']['properties'].items()
                        elif schema['items']['type'] in ('string', ''):
                            return []
                        elif schema['items']['type'] == 'array':
                            return [[]]
                        else:
                            raise (schema['items']['type'])
                    elif type(schema['items']) == list:
                        return []
                    else:
                        raise TypeError(type(schema['items']), schema['items'])
                else:
                    return None
                return self.unpacking_a_dictionary_with_different_questions(schema, properties)

    def unpacking_a_dictionary_with_different_questions(self, schema, dictionary):
        if schema['type'] == 'array':
            key_list = [{}]
        elif schema['type'] == 'object':
            key_list = {}
        else:
            raise TypeError(schema['type'])
        for key, value in dictionary:
            if type(value) == dict and 'type' in value:
                self.write_in_the_stencil(key_list, self.response_stencil(value), key)
            else:
                self.write_in_the_stencil(key_list, None, key)
        return key_list

    def write_in_the_stencil(self, key_list, what_to_write, key):
        if type(key_list) == list:
            key_list[0][key] = what_to_write
        elif type(key_list) == dict:
            key_list[key] = what_to_write
        else:
            raise TypeError(type(key_list))

    def open_ref(self, ref, schema):
        print(schema)
        if type(ref) == str:
            ref = ref.split('/')[1:]
        if len(ref) != 0:
            res = schema[ref[0]]
            return self.open_ref(ref[1:], res)
        else:
            return schema


if __name__ == '__main__':
    schema = {
  "definitions": {
    "Thing": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "default": "Default name"
        }
      }
    }
  },
  "type": "object",
  "properties": {
    "listOfStrings": {
      "type": "array",
      "title": "A list of strings",
      "items": {
        "type": "string",
        "default": "bazinga"
      }
    },
    "multipleChoicesList": {
      "type": "array",
      "title": "A multiple choices list",
      "items": {
        "type": "string",
        "enum": [
          "foo",
          "bar",
          "fuzz",
          "qux"
        ]
      },
      "uniqueItems": True
    },
    "fixedItemsList": {
      "type": "array",
      "title": "A list of fixed items",
      "items": [
        {
          "title": "A string value",
          "type": "string",
          "default": "lorem ipsum"
        },
        {
          "title": "a boolean value",
          "type": "boolean"
        }
      ],
      "additionalItems": {
        "title": "Additional item",
        "type": "number"
      }
    },
    "minItemsList": {
      "type": "array",
      "title": "A list with a minimal number of items",
      "minItems": 3,
      "items": {
        "$ref": "#/definitions/Thing"
      }
    },
    "defaultsAndMinItems": {
      "type": "array",
      "title": "List and item level defaults",
      "minItems": 5,
      "default": [
        "carp",
        "trout",
        "bream"
      ],
      "items": {
        "type": "string",
        "default": "unidentified"
      }
    },
    "nestedList": {
      "type": "array",
      "title": "Nested list",
      "items": {
        "type": "array",
        "title": "Inner list",
        "items": {
          "type": "string",
          "default": "lorem ipsum"
        }
      }
    },
    "unorderable": {
      "title": "Unorderable items",
      "type": "array",
      "items": {
        "type": "string",
        "default": "lorem ipsum"
      }
    },
    "unremovable": {
      "title": "Unremovable items",
      "type": "array",
      "items": {
        "type": "string",
        "default": "lorem ipsum"
      }
    },
    "noToolbar": {
      "title": "No add, remove and order buttons",
      "type": "array",
      "items": {
        "type": "string",
        "default": "lorem ipsum"
      }
    },
    "fixedNoToolbar": {
      "title": "Fixed array without buttons",
      "type": "array",
      "items": [
        {
          "title": "A number",
          "type": "number",
          "default": 42
        },
        {
          "title": "A boolean",
          "type": "boolean",
          "default": False
        }
      ],
      "additionalItems": {
        "title": "A string",
        "type": "string",
        "default": "lorem ipsum"
      }
    }
  }
}

    def print_result(result):
        if type(result) == dict:
            print('==============================')
            for key, value in result.items():
                if type(value) == list:
                    if type(value[0]) == dict:
                        print_result(value)
                    else:
                        print(f'{key} --- {value}')
                else:
                    print(f'{key} --- {value}')
            print('==============================')
        elif type(result) in (tuple, list):
            for value in result:
                print_result(value)
        else:
            print(result)

    Schema = SchemaRead(schema)
    questions_list, stencil = Schema.get()

    print('\n\nquestions_list:')
    print(f'len = {len(questions_list)}')
    print_result(questions_list)

    print('\nstencil:')
    print(stencil)

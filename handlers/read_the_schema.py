from UniTurnip_for_bots.handlers.inline_keyboards import create_custom_keyboards


class SchemaRead:
    def __init__(self, schema):
        self.level = 0
        self.questions_list = []
        self.questions_settings = {}
        self.schema = schema
        self.schema_read(schema)
        self.stencil = self.response_stencil(schema)

    def get(self):
        return self.questions_list, self.stencil

    # ===================================================================================
    # ================================| read_the_schema |================================
    # ===================================================================================
    def schema_read(self, schema, key_before_key=None, penultimate_type=None, last_type=None):
        self.level += 1
        self.q_settings_keys_check(schema, key_before_key)
        for key, value in schema.items():
            if type(value) == dict:
                if 'type' in value.keys():
                    if value['type'] in ('string', 'boolean', 'number', 'integer'):
                        self.questions_creating(key, value, key_before_key, penultimate_type, last_type)
                    else:
                        if 'type' in schema.keys():
                            self.schema_read(value, key_before_key=key, penultimate_type=schema['type'], last_type=value['type'])
                        else:
                            self.schema_read(value, key_before_key=key, penultimate_type=penultimate_type, last_type=value['type'])
                else:
                    self.schema_read(value, key_before_key=key, penultimate_type=penultimate_type, last_type=last_type)
            if type(value) == list:
                for val in value:
                    if type(val) == dict and 'type' in val.keys() and val['type'] in ('string', 'boolean',
                                                                                      'number', 'integer'):
                        self.questions_creating(key, val, key_before_key, penultimate_type, last_type, from_list=True)
        self.level -= 1

    def q_settings_keys_check(self, schema, last_key):
        if self.level not in self.questions_settings.keys():
            self.questions_settings[self.level] = {}
        if 'required' in schema.keys():
            self.questions_settings[self.level]['required'] = schema['required']
        else:
            self.questions_settings[self.level]['required'] = []
        if 'type' in schema.keys():
            self.questions_settings[self.level]['last_key'] = last_key
            if 'title' in schema:
                self.questions_settings[self.level]['title'] = schema['title']
            if 'dependencies' in schema.keys():
                self.questions_settings[self.level]['dependencies'] = schema['dependencies']
            if 'uniqueItems' in schema.keys():
                self.questions_settings[self.level]['uniqueItems'] = schema['uniqueItems']
        max_key = max(self.questions_settings.keys())
        if max_key > self.level:
            self.questions_settings.pop(max_key)

    def questions_creating(self, param_key, schema, key_before_key, penultimate_type, last_type, from_list=False):

        if question := self.required_keys(schema, param_key, penultimate_type=penultimate_type, last_type=last_type):

            if param_key == 'items' and key_before_key == 'items':
                last_key = self.questions_settings[self.level-1]['last_key']
                self.design_for_repeated_question(param_key, question, last_key)
                return
            elif penultimate_type == 'array' and param_key != 'items':
                if self.questions_list and 'type' not in self.questions_list[-1][1]:
                    self.design_for_repeated_question(param_key, question, key_before_key, add_to_last_list=True)
                else:
                    self.design_for_repeated_question(param_key, question, key_before_key)
                return
            elif last_type == 'array':
                if 'enum' not in question.keys() and not from_list:
                    self.design_for_repeated_question(param_key, question, key_before_key)
                else:
                    self.questions_list += [(key_before_key, question)]
                return

            self.questions_list += [(param_key, question)]

    def required_keys(self, schema, param_key, penultimate_type=None, last_type=None):
        q_settings = self.questions_settings[self.level]
        if 'type' not in schema:
            raise KeyError(f'key "type" not in schema. Schema: {schema}')
        question = schema
        if 'title' in question.keys() or 'title' in q_settings.keys():
            question['question'] = question['title'] if 'title' in question.keys() else q_settings['title']
        else:
            return False
        if penultimate_type:
            question['penultimate_type'] = penultimate_type
        if last_type:
            question['last_type'] = last_type
        if 'uniqueItems' in q_settings.keys():
            question['uniqueItems'] = q_settings['uniqueItems']
        question['required'] = True if param_key in q_settings['required'] else False
        question['keyboard'], question['keyboard_settings'] = create_custom_keyboards(question)
        return question

    def design_for_repeated_question(self, param_key, question, key_before_key, add_to_last_list=False):
        more_question = self.required_keys({'title': 'Еще?', 'type': 'more_q'}, param_key)
        if add_to_last_list:
            last_q_list = self.questions_list[-1][1]
            last_q_key = max(last_q_list.keys())
            last_q_list[last_q_key] = (param_key, question)
            last_q_list[last_q_key + 1] = ('UniTurnipMore', more_question)
            self.questions_list[-1] = (key_before_key, last_q_list)
        else:
            dict_with_questions = {0: (param_key, question), 1: ('UniTurnipMore', more_question)}
            self.questions_list += [(key_before_key, dict_with_questions)]

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
    from UniTurnip_for_bots.handlers.constants import *
    schema = Arrays

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

test ={
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
}




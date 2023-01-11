from UniTurnip_for_bots.handlers.inline_keyboards import create_custom_keyboards, optional_keyboard


class SchemaRead:
    def __init__(self):
        self.questions_list = []
        self.last_type = None
        self.required = []
        self.last_key = None
        print(optional_keyboard)

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
            if 'description' in schema_.keys():
                question['question'] += f'\n{schema_["description"]}'
            question['required'] = True if param_key_ in self.required else False
            question['last_type'] = self.last_type
            question['keyboard'], question['keyboard_settings'] = create_custom_keyboards(question)
            print('==================')
            print(question['keyboard'])
            return question

        if question := required_keys(param_key, schema):

            question['answer_settings'] = {}
            if 'minLength' in schema.keys():
                question['answer_settings']['minLength'] = schema['minLength']

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

    def response_stencil(self, schema):
        if type(schema) == dict:
            if 'type' in schema:

                if 'properties' in schema.keys():
                    properties = schema['properties'].items()
                elif 'items' in schema.keys() and 'properties' in schema['items']:
                    properties = schema['items']['properties'].items()
                elif 'items' in schema.keys() and 'properties' not in schema['items']:
                    properties = schema['items'].items()
                else:
                    return None

                if schema['type'] == 'array':
                    key_list = [{}]
                elif schema['type'] == 'object':
                    key_list = {}
                else:
                    raise TypeError(schema['type'])

                for key, value in properties:
                    if type(value) == dict and 'type' in value:
                        self.write_in_the_stencil(key_list, self.response_stencil(value), key)
                    else:
                        self.write_in_the_stencil(key_list, None, key)
                return key_list
            else:
                return None
        else:
            return None

    def write_in_the_stencil(self, key_list, what_to_write, key):
        if type(key_list) == list:
            key_list[0][key] = what_to_write
        elif type(key_list) == dict:
            key_list[key] = what_to_write
        else:
            raise TypeError(type(key_list))

if __name__ == '__main__':
    schema = {
  "title": "A list of tasks",
  "type": "object",
  "required": [
    "title"
  ],
  "properties": {
    "title": {
      "type": "string",
      "title": "Task list title"
    },
    "tasks": {
      "type": "array",
      "title": "Tasks",
      "items": {
        "type": "object",
        "required": [
          "title"
        ],
        "properties": {
          "title": {
            "type": "string",
            "title": "Title",
            "description": "A sample title"
          },
          "details": {
            "type": "string",
            "title": "Task details",
            "description": "Enter the task details"
          },
          "done": {
            "type": "boolean",
            "title": "Done?",
            "default": False
          }
        }
      }
    }
  }
}
    Schema = SchemaRead()

    Schema.schema_read(schema)
    print('\n\nResult:')
    print(f'len = {len(Schema.questions_list)}')

    for value in Schema.questions_list:
        print(value)
        for key, val in value[1].items():
            print(f'{key} --- {val}')
        print('dict end')

    print(Schema.response_stencil(schema))

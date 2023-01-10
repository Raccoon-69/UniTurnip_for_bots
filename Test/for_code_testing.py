from UniTurnip_for_bots.handlers.keyboards.inline_keyboards import create_custom_keyboards


class test_test:
    def __init__(self):
        self.order = None
        self.questions_list = []

    def object_unpack(self, schema: dict):
        # 'required - []'
        # 'type - "string", "array", "object", "boolean", "number"'
        #     'if type = array - items'
        # 'title'
        # 'properties - {}'
        # 'description'
        # 'default'
        required = [] if 'required' not in schema.keys() else schema['required']
        if 'properties' not in schema:
            print(schema)
            print('continue')
            return
        for param_key, parameters in schema['properties'].items():
            if 'type' in parameters.keys():
                if parameters['type'] == 'string':
                    self.string_unpack(param_key, parameters, required)
                elif parameters['type'] == 'array':
                    self.array_unpack(param_key, parameters, required)
                elif parameters['type'] == 'boolean':
                    pass
                elif parameters['type'] == 'object':
                    self.object_unpack(parameters)
                else:
                    print(f'type "{parameters["type"]}" passed')

    def array_unpack(self, param_key, parameters, required):
        # 'type'
        # 'title'
        # 'items' !!!
        questions_settings = self.get_default_settings(parameters)
        if type(parameters['items']) == list:
            return

        if 'enum' in parameters['items'].keys():
            questions_settings['enum'] = parameters['items']['enum']
            questions_settings['keyboard'] = self.get_custom_keyboard(questions_settings)
        else:
            questions_settings = self.get_optional_keyboard(param_key, required, questions_settings)
        self.questions_list += [(param_key, questions_settings)]

    def string_unpack(self, param_key, parameters, required):
        questions_settings = self.get_default_settings(parameters)
        questions_settings = self.get_optional_keyboard(param_key, required, questions_settings)
        if 'minLength' in parameters.keys():
            questions_settings['answer_settings']['minLength'] = parameters['minLength']
        self.questions_list += [(param_key, questions_settings)]

    def get_default_settings(self, parameters):
        q_settings = {
            'type': parameters['type'],
            'questions': '' if 'title' not in parameters else parameters['title']
        }
        q_settings['questions'] += '' if 'description' not in parameters.keys() else f'\n{parameters["description"]}'
        return q_settings

    def get_optional_keyboard(self, param_key, required, questions_settings):
        if param_key in required:
            questions_settings['keyboard'] = ['optional_keyboard']
            questions_settings['answer_settings'] = {'cancel': True}
        else:
            questions_settings['keyboard'] = None
            questions_settings['answer_settings'] = {'cancel': False}
        return questions_settings

    def get_custom_keyboard(self, keys):
        return create_custom_keyboards(keys)


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
    test = test_test()
    test.object_unpack(schema)
    result = test.questions_list
    for res in result:
        print(res)

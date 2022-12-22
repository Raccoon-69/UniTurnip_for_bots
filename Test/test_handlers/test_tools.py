from unittest import TestCase, main

from UniTurnip_for_bots.handlers.tools import read_schema, str_to_dict, schema_error_check


class TestTools(TestCase):
    def test_read_schema(self):
        schema = '''{
          "title": "A registration form",
          "description": "A simple form example.",
          "type": 'object',
          "required": [
            "firstName",
            'lastName'
          ],
          "properties": {
            "firstName": {
              "type": 'string',
              "title": "First name",
              "default": 'Chuck'
            },
            "lastName": {
              "type": "string",
              'title': "Last name"
            },
            'telephone': {
              "type": "string",
              "title": "Telephone",
              'minLength': 10
            }
          }
        }'''
        schema_result = {
          "title": "A registration form",
          "description": "A simple form example.",
          "type": "object",
          "required": [
            "firstName",
            "lastName"
          ],
          "properties": {
            "firstName": {
              "type": "string",
              "title": "First name",
              "default": "Chuck"
            },
            "lastName": {
              "type": "string",
              "title": "Last name"
            },
            "telephone": {
              "type": "string",
              "title": "Telephone",
              "minLength": 10
            }
          }
        }
        self.assertEqual(read_schema(schema), schema_result)
        self.assertEqual(read_schema(schema_result), schema_result)

    def test_str_to_dict(self):
        schema = '''{
                  'title': "A registration form",
                  'description': "A simple form example.",
                  "type": "object",
                  'required': [
                    "firstName",
                    "lastName"
                  ],
                  "properties": {
                    "firstName": {
                      "type": "string",
                      "title": "First name",
                      "default": 'Chuck'
                    },
                    "lastName": {
                      "type": "string",
                      "title": "Last name"
                    },
                    'telephone': {
                      "type": "string",
                      "title": 'Telephone',
                      'minLength': 10
                    }
                  }
                }'''
        schema_result = {
            "title": "A registration form",
            "description": "A simple form example.",
            "type": "object",
            "required": [
                "firstName",
                "lastName"
            ],
            "properties": {
                "firstName": {
                    "type": "string",
                    "title": "First name",
                    "default": "Chuck"
                },
                "lastName": {
                    "type": "string",
                    "title": "Last name"
                },
                "telephone": {
                    "type": "string",
                    "title": "Telephone",
                    "minLength": 10
                }
            }
        }
        self.assertEqual(str_to_dict(schema), schema_result)
        with self.assertRaises(TypeError):
            str_to_dict(928349)
            str_to_dict([23,42,34])

    def test_schema_error_check(self):
        schema_marriage0 = {
            'error note': 'No keys "required" and "properties"'
        }
        schema_marriage1 = {
            'error note': 'No keys "type" and "title" in properties "name"',
            'required': [],
            'properties': {
                'name': {
                    'name': ''
                }
            }
        }
        with self.assertRaises(KeyError):
            schema_error_check(schema_marriage0)
        with self.assertRaises(KeyError):
            schema_error_check(schema_marriage1)


if __name__ == '__main__':
    main()

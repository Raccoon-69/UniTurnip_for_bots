from unittest import TestCase, main
from UniTurnip_for_bots import UniTurnip
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

UniTurnip = UniTurnip()


class TestUniTurnip(TestCase):
    def test(self):
        schema1 = '''{
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
        schema2 = {
            "title": "A registration form",
            "description": "A simple form example.",
            "type": "object",
            "required": [
                "firstName",
                "lastName"
            ],
            "properties": {
                "telephone": {
                    "type": "string",
                    "title": "Telephone",
                    "minLength": 10
                },
                "firstName": {
                    "type": "string",
                    "title": "First name",
                    "default": "Chuck"
                },
                "lastName": {
                    "type": "string",
                    "title": "Last name"
                },
            }
        }
        required = ["firstName", "lastName"]
        properties = {
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
        questions_keys = ('firstName', 'lastName', 'telephone')
        self.assertEqual(UniTurnip.scheme_not_definite, True)

        # test read_json func
        UniTurnip.read_json(schema1)
        self.assertEqual(UniTurnip.required, required)
        self.assertEqual(UniTurnip.properties, properties)
        self.assertEqual(UniTurnip.questions_keys, questions_keys)
        self.assertEqual(UniTurnip.scheme_not_definite, False)

        # test read_json func
        UniTurnip.read_json(schema2)
        self.assertEqual(UniTurnip.required, required)
        self.assertEqual(UniTurnip.properties, properties)
        self.assertEqual(UniTurnip.questions_keys, questions_keys)
        self.assertEqual(UniTurnip.scheme_not_definite, False)

        # test start_survey func
        current_question_settings = {
            "type": "string",
            "title": "First name",
            "default": "Chuck"
        }
        UniTurnip.start_survey()
        self.assertEqual(UniTurnip.current_state_num, 1)
        self.assertEqual(UniTurnip.processing, True)
        self.assertEqual(UniTurnip.current_state_name, 'firstName')
        self.assertEqual(UniTurnip.current_question_settings, current_question_settings)
        self.assertEqual(UniTurnip.current_question, 'First name')
        self.assertEqual(UniTurnip.current_keyboard, None)
        # self.assertEqual(self.UniTurnip.current_callback_data, None)

        # test next func
        current_question_settings1 ={
            "type": "string",
            "title": "Last name"
        }
        UniTurnip.next()
        self.assertEqual(UniTurnip.current_state_num, 2)
        self.assertEqual(UniTurnip.current_state_name, 'lastName')
        self.assertEqual(UniTurnip.current_question_settings, current_question_settings1)
        self.assertEqual(UniTurnip.current_question, 'Last name')
        self.assertEqual(UniTurnip.current_keyboard, None)

        # test next func
        UniTurnip.next()
        current_question_settings2 = {
            "type": "string",
            "title": "Telephone",
            "minLength": 10
        }
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text='Пропустить', callback_data='cancel')
                ]
            ]
        )
        self.assertEqual(UniTurnip.current_state_num, 3)
        self.assertEqual(UniTurnip.current_state_name, 'telephone')
        self.assertEqual(UniTurnip.current_question_settings, current_question_settings2)
        self.assertEqual(UniTurnip.current_question, 'Telephone')
        self.assertEqual(UniTurnip.current_keyboard, keyboard)

        # test next func
        UniTurnip.next()
        self.assertEqual(UniTurnip.current_state_num, 4)
        self.assertEqual(UniTurnip.current_state_name, None)
        self.assertEqual(UniTurnip.processing, False)

        # test next func
        UniTurnip.next()
        self.assertEqual(UniTurnip.current_state_num, 5)
        self.assertEqual(UniTurnip.current_state_name, None)
        self.assertEqual(UniTurnip.processing, False)

        # test back func
        UniTurnip.back()
        self.assertEqual(UniTurnip.current_state_num, 4)
        self.assertEqual(UniTurnip.current_state_name, None)
        self.assertEqual(UniTurnip.processing, False)

        # test back func
        UniTurnip.back()
        current_question_settings2 = {
            "type": "string",
            "title": "Telephone",
            "minLength": 10
        }
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text='Пропустить', callback_data='cancel')
                ]
            ]
        )
        self.assertEqual(UniTurnip.current_state_num, 3)
        self.assertEqual(UniTurnip.current_state_name, 'telephone')
        self.assertEqual(UniTurnip.current_question_settings, current_question_settings2)
        self.assertEqual(UniTurnip.current_question, 'Telephone')
        self.assertEqual(UniTurnip.current_keyboard, keyboard)

        # test answer func
        UniTurnip.answer('5631')
        self.assertEqual(UniTurnip.user_answers, {})
        current_question_settings1 ={
            "type": "string",
            "title": "Last name"
        }
        self.assertEqual(UniTurnip.current_state_num, 2)
        self.assertEqual(UniTurnip.current_state_name, 'lastName')
        self.assertEqual(UniTurnip.current_question_settings, current_question_settings1)
        self.assertEqual(UniTurnip.current_question, 'Last name')
        self.assertEqual(UniTurnip.current_keyboard, None)

        # test answer func
        UniTurnip.next()
        current_question_settings2 = {
            "type": "string",
            "title": "Telephone",
            "minLength": 10
        }
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Пропустить', callback_data='cancel')
            ]
        ]
        )
        self.assertEqual(UniTurnip.current_state_num, 3)
        self.assertEqual(UniTurnip.current_state_name, 'telephone')
        self.assertEqual(UniTurnip.current_question_settings, current_question_settings2)
        self.assertEqual(UniTurnip.current_question, 'Telephone')
        self.assertEqual(UniTurnip.current_keyboard, keyboard)
        UniTurnip.answer('1234567890')
        self.assertEqual(UniTurnip.user_answers, {'telephone': '1234567890'})


if __name__ == '__main__':
    main()

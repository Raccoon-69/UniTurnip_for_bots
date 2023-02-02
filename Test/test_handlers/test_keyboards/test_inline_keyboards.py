from unittest import TestCase, main
from UniTurnip_for_bots.handlers.inline_keyboards import create_custom_keyboards, keyboard_for_more_q, \
    assembly_and_required_button
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class TestInlineKeyboardsFile(TestCase):

    def test_create_custom_keyboards(self):
        # required question with type string
        correct_answer = (
            None,
            ['string']
        )
        settings = {
            'required': True,
            'type': 'string',
        }
        self.assertEqual(create_custom_keyboards(settings), correct_answer)

        # required question with type string
        cancel_button = [[InlineKeyboardButton(text='Skip', callback_data='UniTurnipCancel')]]
        correct_answer = (
            InlineKeyboardMarkup(inline_keyboard=cancel_button),
            ['string', 'cancel']
        )
        settings = {
            'required': False,
            'type': 'string',
        }
        self.assertEqual(create_custom_keyboards(settings), correct_answer)

        settings = {
            'required': True,
            'enum': ['first', 'second', 'third']
        }
        buttons = [
            [
                InlineKeyboardButton(text='first', callback_data='UniTurnip_first'),
                InlineKeyboardButton(text='second', callback_data='UniTurnip_second'),
                InlineKeyboardButton(text='third', callback_data='UniTurnip_third')
            ]
        ]
        correct_answer = (
            InlineKeyboardMarkup(inline_keyboard=buttons),
            ['custom']
        )
        print(correct_answer)
        self.assertEqual(create_custom_keyboards(settings), correct_answer)

        settings = {
            'type': 'boolean',
            'required': True

        }
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Yes', callback_data='UniTurnipTrue'),
                    InlineKeyboardButton(text='No', callback_data='UniTurnipFalse')
                ]
            ])
        correct_answer = (keyboard, ['boolean'])
        self.assertEqual(create_custom_keyboards(settings), correct_answer)

        settings = {
            'type': 'boolean',
            'required': False

        }
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Yes', callback_data='UniTurnipTrue'),
                    InlineKeyboardButton(text='No', callback_data='UniTurnipFalse')
                ],
                [
                    InlineKeyboardButton(text='Skip', callback_data='UniTurnipCancel')
                ]
            ])
        correct_answer = (keyboard, ['boolean', 'cancel'])
        self.assertEqual(create_custom_keyboards(settings), correct_answer)

        # settings = {
        #     'type': '',
        #     'required': False,
        #     'enum': ['first', 'second', 'third']
        # }
        # buttons = [
        #     [
        #         InlineKeyboardButton(text='first', callback_data='UniTurnip_first'),
        #         InlineKeyboardButton(text='second', callback_data='UniTurnip_second'),
        #         InlineKeyboardButton(text='third', callback_data='UniTurnip_third')
        #     ],
        #     [
        #         InlineKeyboardButton(text='Skip', callback_data='UniTurnipCancel')
        #     ]
        # ]
        # correct_answer = (
        #     InlineKeyboardMarkup(inline_keyboard=buttons),
        #     ['custom']
        # )
        # self.assertEqual(create_custom_keyboards(settings), correct_answer)

    def test_keyboard_for_more_q(self):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='More', callback_data='UniTurnipMore'),
                    InlineKeyboardButton(text='Accept', callback_data='UniTurnipNotMore')
                ]
            ])
        correct_answer = (keyboard, ['more'])
        self.assertEqual(keyboard_for_more_q(), correct_answer)

    def test_assembly_and_required_button(self):
        settings = {
            'required': True
        }
        buttons = [[]]
        keyboard_type = ['string', 'other_type']
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [],
                [
                    InlineKeyboardButton(text='Skip', callback_data='UniTurnipCancel')
                ]
            ]
        )
        correct_answer = (keyboard, ['string', 'other_type', 'cancel'])
        self.assertEqual(assembly_and_required_button(settings, buttons, keyboard_type), correct_answer)

        settings = {
            'required': False
        }
        buttons = [[
            InlineKeyboardButton(text='Some kind button', callback_data='UniTurnip_Some kind button'),
            InlineKeyboardButton(text='Other button', callback_data='UniTurnip_Other button')
        ]]
        keyboard_type = ['string', 'other_type', 'custom']
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Some kind button', callback_data='UniTurnip_Some kind button'),
                    InlineKeyboardButton(text='Other button', callback_data='UniTurnip_Other button')
                ],
                [
                    InlineKeyboardButton(text='Skip', callback_data='UniTurnipCancel')
                ]
            ]
        )
        correct_answer = (keyboard, ['string', 'other_type', 'custom', 'cancel'])
        self.assertEqual(assembly_and_required_button(settings, buttons, keyboard_type), correct_answer)


if __name__ == '__main__':
    main()

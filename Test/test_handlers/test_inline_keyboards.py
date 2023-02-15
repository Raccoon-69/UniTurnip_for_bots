from unittest import TestCase, main
from UniTurnip_for_bots.handlers.inline_keyboards import get_keyboards, keyboard_for_more_q, \
    assembly_and_required_button
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class TestInlineKeyboardsFile(TestCase):

    def test_create_custom_keyboards(self):
        # ========== required question with type string ==========
        settings = {
            'required': True,
            'type': 'string',
        }
        correct_answer = (
            None,
            ['string']
        )
        self.assertEqual(get_keyboards(settings), correct_answer)
        settings = {
            'required': False,
            'type': 'string',
        }
        self.assertEqual(get_keyboards(settings, required=True), correct_answer)

        settings = {
            'required': False,
            'type': 'string',
        }
        cancel_button = [[InlineKeyboardButton(text='Skip', callback_data='UniTurnipCancel')]]
        correct_answer = (
            InlineKeyboardMarkup(inline_keyboard=cancel_button),
            ['string']
        )
        self.assertEqual(get_keyboards(settings), correct_answer)
        settings = {
            'required': True,
            'type': 'string',
        }
        self.assertEqual(get_keyboards(settings, required=False), correct_answer)

        # ========== with custom buttons ==========
        settings = {
            'type': 'string',
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
            ['string', 'custom']
        )
        self.assertEqual(get_keyboards(settings), correct_answer)
        settings = {
            'type': 'string',
            'required': False,
            'enum': ['first', 'second', 'third']
        }
        self.assertEqual(get_keyboards(settings, required=True), correct_answer)

        settings = {
            'type': 'string',
            'required': False,
            'enum': ['first', 'second', 'third']
        }
        buttons = [
            [
                InlineKeyboardButton(text='first', callback_data='UniTurnip_first'),
                InlineKeyboardButton(text='second', callback_data='UniTurnip_second'),
                InlineKeyboardButton(text='third', callback_data='UniTurnip_third')
            ],
            [
                InlineKeyboardButton(text='Skip', callback_data='UniTurnipCancel')
            ]
        ]
        correct_answer = (
            InlineKeyboardMarkup(inline_keyboard=buttons),
            ['string', 'custom']
        )
        self.assertEqual(get_keyboards(settings), correct_answer)


        # ========== type boolean ==========
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
        self.assertEqual(get_keyboards(settings), correct_answer)
        settings = {
            'type': 'boolean',
            'required': False
        }
        self.assertEqual(get_keyboards(settings, required=True), correct_answer)

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
        correct_answer = (keyboard, ['boolean'])
        self.assertEqual(get_keyboards(settings), correct_answer)
        settings = {
            'type': 'boolean',
            'required': True
        }
        self.assertEqual(get_keyboards(settings, required=False), correct_answer)

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
            'type': 'string',
            'required': False
        }
        buttons = [[]]
        keyboard_type = ['string']
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [],
                [
                    InlineKeyboardButton(text='Skip', callback_data='UniTurnipCancel')
                ]
            ]
        )
        correct_answer = (keyboard, ['string'])
        self.assertEqual(assembly_and_required_button(settings, buttons, keyboard_type), correct_answer)

        settings = {
            'required': False
        }
        buttons = [[
            InlineKeyboardButton(text='Some kind button', callback_data='UniTurnip_Some kind button'),
            InlineKeyboardButton(text='Other button', callback_data='UniTurnip_Other button')
        ]]
        keyboard_type = ['string', 'custom']
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
        correct_answer = (keyboard, ['string', 'custom'])
        self.assertEqual(assembly_and_required_button(settings, buttons, keyboard_type), correct_answer)


if __name__ == '__main__':
    main()
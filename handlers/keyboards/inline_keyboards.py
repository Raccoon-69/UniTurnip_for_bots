from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text



optional_questions = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Пропустить', callback_data='cancel')
        ]
    ]
)
optional_callback_data = Text(equals=['cancel'])

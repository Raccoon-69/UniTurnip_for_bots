from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


optional_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Пропустить', callback_data='UniTurnipCancel')
        ]
    ]
)


boolean_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='UniTurnipTrue'),
            InlineKeyboardButton(text='Нет', callback_data='UniTurnipFalse')
        ]
    ]
)


for_more_questions_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Еще', callback_data='UniTurnipMore'),
            InlineKeyboardButton(text='Нет', callback_data='UniTurnipNotMore')
        ]
    ]
)


def get_keyboard(settings):
    if settings['type'] == 'string':
        if not settings['required']:
            return optional_keyboard, ['cancel']
        return None, []
    elif settings['type'] == 'boolean':
        if not settings['required']:
            return boolean_keyboard, ['boolean', 'cancel']
        return boolean_keyboard, ['boolean']
    elif settings['type'] == 'array':
        return create_custom_keyboards(settings),
    elif settings['type'] == 'settings':
        return for_more_questions_keyboard, ['more']


def create_custom_keyboards(settings):
    buttons = []
    for key in settings['enum']:
        buttons += [InlineKeyboardButton(text=key, callback_data=f'UniTurnip_{key}')]
    custom_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return custom_keyboard

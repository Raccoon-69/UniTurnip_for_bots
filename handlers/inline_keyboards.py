from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_custom_keyboards(settings, other=None):
    if other:
        keyboard_type = other
    else:
        keyboard_type = []

    if 'enum' in settings.keys():
        buttons = [[]]
        for key in settings['enum']:
            buttons[0] += [InlineKeyboardButton(text=key, callback_data=f'UniTurnip_{key}')]
        buttons += [[InlineKeyboardButton(text='Accept', callback_data='UniTurnipNotMore')]]
        keyboard_type += ['custom']
        return InlineKeyboardMarkup(inline_keyboard=buttons), keyboard_type
    else:
        if settings['type'] in ('string', 'integer', 'number'):
            keyboard_type = [settings['type']]
            return assembly_and_required_button(settings, [], keyboard_type, assembly=False)
        elif settings['type'] == 'more_q':
            buttons = [[
                InlineKeyboardButton(text='More', callback_data='UniTurnipMore'),
                InlineKeyboardButton(text='Accept', callback_data='UniTurnipNotMore')
            ]]
            keyboard_type += ['more']
            return InlineKeyboardMarkup(inline_keyboard=buttons), keyboard_type
        elif settings['type'] == 'boolean':
            buttons = [[
                InlineKeyboardButton(text='Yes', callback_data='UniTurnipTrue'),
                InlineKeyboardButton(text='No', callback_data='UniTurnipFalse')
            ]]
            keyboard_type += ['boolean']
        else:
            raise TypeError(settings['type'])
    return assembly_and_required_button(settings, buttons, keyboard_type)


def assembly_and_required_button(settings, buttons, keyboard_type, assembly=True):
    if not settings['required']:
        buttons += [[InlineKeyboardButton(text='Cancel', callback_data='UniTurnipCancel')]]
        keyboard_type += ['cancel']
        return InlineKeyboardMarkup(inline_keyboard=buttons), keyboard_type
    if assembly:
        return InlineKeyboardMarkup(inline_keyboard=buttons), keyboard_type
    return None, keyboard_type


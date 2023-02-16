from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboards(settings, required=None):
    if 'enum' in settings.keys():
        return get_custom_keyboard(settings, [settings['type'], 'custom'], required=required)
    elif settings['type'] == 'string':
        return assembly_and_required_button(settings, [[]], ['string'], required=required)
    elif settings['type'] == 'integer':
        return get_integer_keyboard(settings, ['integer'], whole_numbers=True, required=required)
    elif settings['type'] == 'number':
        return get_integer_keyboard(settings, ['number'], whole_numbers=False, required=required)
    elif settings['type'] == 'boolean':
        return get_boolean_keyboard(settings, ['boolean'], required=required)
    else:
        raise TypeError(settings['type'])


def get_integer_keyboard(settings, keyboard_type, whole_numbers=True, required=None):
    number_button = get_number_button()
    if not whole_numbers:
        number_button += [
            [
                InlineKeyboardButton(text='C', callback_data='UniTurnipClear'),
                InlineKeyboardButton(text='0', callback_data='UniTurnip0'),
                InlineKeyboardButton(text='>>>', callback_data='UniTurnipFurther')
            ]
        ]
    else:
        number_button += [
            [
                InlineKeyboardButton(text='C', callback_data='UniTurnipClear'),
                InlineKeyboardButton(text='0', callback_data='UniTurnip0'),
                InlineKeyboardButton(text=',', callback_data='UniTurnipComma')
            ],
            [
                InlineKeyboardButton(text='>>>', callback_data='UniTurnipFurther')
            ]
        ]
    return assembly_and_required_button(settings, number_button, keyboard_type, required=required)


def get_boolean_keyboard(settings, keyboard_type, required=None):
    buttons = [[
        InlineKeyboardButton(text='Yes', callback_data='UniTurnipTrue'),
        InlineKeyboardButton(text='No', callback_data='UniTurnipFalse')
    ]]
    return assembly_and_required_button(settings, buttons, keyboard_type, required=required)


def get_custom_keyboard(settings, keyboard_type, required=None):
    buttons = [[]]
    for key in settings['enum']:
        buttons[0] += [InlineKeyboardButton(text=key, callback_data=f'UniTurnip_{key}')]
    return assembly_and_required_button(settings, buttons, keyboard_type, required=required)


def get_number_button():
    return [
        [
            InlineKeyboardButton(text='1', callback_data='UniTurnip1'),
            InlineKeyboardButton(text='2', callback_data='UniTurnip2'),
            InlineKeyboardButton(text='3', callback_data='UniTurnip3')
        ],
        [

            InlineKeyboardButton(text='4', callback_data='UniTurnip4'),
            InlineKeyboardButton(text='5', callback_data='UniTurnip5'),
            InlineKeyboardButton(text='6', callback_data='UniTurnip6')
        ],
        [
            InlineKeyboardButton(text='7', callback_data='UniTurnip7'),
            InlineKeyboardButton(text='8', callback_data='UniTurnip8'),
            InlineKeyboardButton(text='9', callback_data='UniTurnip9')
        ],
    ]


def assembly_and_required_button(settings, buttons, keyboard_type, required=None):
    if required is not None:
        if not buttons[0] or not buttons[0][0]:
            if required:
                return None, keyboard_type
            else:
                return assembly_with_skip_button(buttons, keyboard_type)
        else:
            if required:
                return InlineKeyboardMarkup(inline_keyboard=buttons), keyboard_type
            else:
                return assembly_with_skip_button(buttons, keyboard_type)
    else:
        if not buttons[0] or not buttons[0][0]:
            if not settings['required'] and 'minItems' not in settings.keys():
                return assembly_with_skip_button(buttons, keyboard_type)
            else:
                return None, keyboard_type
        elif not settings['required'] and 'minItems' not in settings.keys():
            return assembly_with_skip_button(buttons, keyboard_type)
        else:
            return InlineKeyboardMarkup(inline_keyboard=buttons), keyboard_type


def assembly_with_skip_button(buttons, keyboard_type):
    with_skip_button = buttons + [[InlineKeyboardButton(text='Skip', callback_data='UniTurnipCancel')]]
    if not buttons[0] or not buttons[0][0]:
        return {'with_skip': (InlineKeyboardMarkup(inline_keyboard=with_skip_button), keyboard_type),
                'without_skip': (None, keyboard_type)}
    return {'with_skip': (InlineKeyboardMarkup(inline_keyboard=with_skip_button), keyboard_type),
            'without_skip': (InlineKeyboardMarkup(inline_keyboard=buttons), keyboard_type)}


def keyboard_for_more_q():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='More', callback_data='UniTurnipMore'),
                InlineKeyboardButton(text='Accept', callback_data='UniTurnipNotMore')
            ]
        ])
    return keyboard, ['more']

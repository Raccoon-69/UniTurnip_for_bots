class ButtonResponsePrecessing:
    def __init__(self, dict_with_func_from_main):
        self.dict_with_func_from_main = dict_with_func_from_main

    def processing(self, button, current_question):
        if button == 'UniTurnipCancel' and 'cancel' in current_question['keyboard_settings']:
            self.dict_with_func_from_main['next']()
        elif button in ('UniTurnipMore', 'UniTurnipNotMore') and 'more' in current_question['keyboard_settings']:
            if button == 'UniTurnipNotMore':
                self.dict_with_func_from_main['next']()
            else:
                self.dict_with_func_from_main['back']()
        elif button in ('UniTurnipTrue', 'UniTurnipFalse') and 'boolean' in current_question['keyboard_settings']:
            answer = True if button == 'UniTurnipTrue' else False
            self.dict_with_func_from_main['save_and_next'](answer)
        elif 'custom' in current_question['keyboard_settings']:
            answer = button.strip('UniTurnip_')
            self.dict_with_func_from_main['save_and_next'](answer)

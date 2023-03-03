class State:
    def __init__(self, questions_list):
        self.current_state_num = [0]
        self.questions_list = questions_list
        self.processing = None

    def initialization(self):
        self.processing = True
        current_question, self.current_state_num = get_question(self.questions_list)
        return current_question

    def next(self):
        self.current_state_num[-1] += 1
        return self.question()

    def last(self):
        self.current_state_num[-1] -= 1
        return self.question()

    def question(self):
        if self.current_main_q_in_list():
            question = get_current_question(self.questions_list, self.current_state_num)
            if question == []:
                return self.end()
            if type(question) == list:
                current_question, current_state_num = get_question(question)
                self.current_state_num += current_state_num
                return current_question
            elif type(question) == tuple:
                if type(question[1]) == list:
                    current_question, current_state_num = get_question(question[1])
                    self.current_state_num += [1] + current_state_num
                    return current_question
            return question
        else:
            if len(self.current_state_num) == 1:
                return self.next()
            self.current_state_num = self.current_state_num[:-1]
            if type(self.current_state_num) == int:
                return self.end()
            return self.next()

    def end(self):
        self.processing = False
        self.current_state_num = None
        return None

    def current_main_q_in_list(self):
        curr_main_q_num = self.current_state_num[-1]
        if len(self.current_state_num) == 1:
            return -1 < curr_main_q_num <= len(self.questions_list)
        questions_list = get_current_question(self.questions_list, self.current_state_num)
        return -1 < curr_main_q_num <= len(questions_list)


def get_question(questions):
    if type(questions[0]) == list:
        question, numbers = get_question(questions[0])
        return question, [0] + numbers
    elif type(questions[0]) == tuple and type(questions[0][1]) == str and type(questions[0][1]) == list:
        question, numbers = get_question(questions[0][1])
        return question, [0] + numbers
    elif type(questions[0]) in (dict, tuple):
        return questions[0], [0]
    else:
        raise TypeError(type(questions))


def get_current_question(question, num):
    if type(num) == list:
        if len(num) != 0:
            if len(question) <= num[0]:
                return []
            return get_current_question(question[num[0]], num[1:])
    elif type(num) == int:
        return question[num]
    return question


if __name__ == '__main__':
    Simple = [('firstName', (None, ['string'])), ('lastName', (None, ['string'])), ('telephone', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])})]
    Nested = [('first', (None, ['string'])), ('tasks', [('title', (None, ['string'])), ('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])})])]
    Arrays = [('listOfStrings', {'type': 'string', 'default': 'bazinga', 'question': 'A list of strings', 'main_type': 'object', 'required': False, 'last_key': 'listOfStrings', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'A list of strings', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('multipleChoicesList', {'type': 'string', 'enum': ['foo', 'bar', 'fuzz', 'qux'], 'question': 'A multiple choices list', 'main_type': 'object', 'required': False, 'last_key': 'multipleChoicesList', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'A multiple choices list', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('fixedItemsList', [{'title': 'A string value', 'type': 'string', 'default': 'lorem ipsum', 'question': 'A string value', 'main_type': 'object', 'required': True, 'last_key': 'fixedItemsList', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'A list of fixed items', 'keyboard': None, 'settings': ['string']}, {'title': 'a boolean value', 'type': 'boolean', 'question': 'a boolean value', 'main_type': 'object', 'required': True, 'last_key': 'fixedItemsList', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'A list of fixed items', 'keyboard': {"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, 'settings': ['boolean']}, {'title': 'Additional item', 'type': 'number', 'question': 'Additional item', 'main_type': 'object', 'required': False, 'last_key': 'fixedItemsList', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'A list of fixed items', 'keyboard': 'with_skip', 'settings': 'without_skip'}]), ('minItemsList', [('name', {'type': 'string', 'default': 'Default name', 'question': 'A list with a minimal number of items', 'main_type': 'object', 'required': False, 'last_key': 'minItemsList', 'last_object_data': {'main_type': 'object', 'required': [], 'last_key': 'minItemsList', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'A list with a minimal number of items'}, 'keyboard': 'with_skip', 'settings': 'without_skip'})]), ('defaultsAndMinItems', {'type': 'string', 'default': 'unidentified', 'question': 'List and item level defaults', 'main_type': 'object', 'required': False, 'last_key': 'defaultsAndMinItems', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'List and item level defaults', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('nestedList', {'type': 'string', 'default': 'lorem ipsum', 'question': 'Inner list', 'main_type': 'object', 'required': False, 'last_key': 'nestedList', 'last_object_data': {'main_type': 'object', 'required': [], 'last_key': 'nestedList', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'Nested list'}, 'main_title': 'Inner list', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('unorderable', {'type': 'string', 'default': 'lorem ipsum', 'question': 'Unorderable items', 'main_type': 'object', 'required': False, 'last_key': 'unorderable', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'Unorderable items', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('unremovable', {'type': 'string', 'default': 'lorem ipsum', 'question': 'Unremovable items', 'main_type': 'object', 'required': False, 'last_key': 'unremovable', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'Unremovable items', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('noToolbar', {'type': 'string', 'default': 'lorem ipsum', 'question': 'No add, remove and order buttons', 'main_type': 'object', 'required': False, 'last_key': 'noToolbar', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'No add, remove and order buttons', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('fixedNoToolbar', [{'title': 'A number', 'type': 'number', 'default': 42, 'question': 'A number', 'main_type': 'object', 'required': True, 'last_key': 'fixedNoToolbar', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'Fixed array without buttons', 'keyboard': {"inline_keyboard": [[{"text": "1", "callback_data": "UniTurnip1"}, {"text": "2", "callback_data": "UniTurnip2"}, {"text": "3", "callback_data": "UniTurnip3"}], [{"text": "4", "callback_data": "UniTurnip4"}, {"text": "5", "callback_data": "UniTurnip5"}, {"text": "6", "callback_data": "UniTurnip6"}], [{"text": "7", "callback_data": "UniTurnip7"}, {"text": "8", "callback_data": "UniTurnip8"}, {"text": "9", "callback_data": "UniTurnip9"}], [{"text": "C", "callback_data": "UniTurnipClear"}, {"text": "0", "callback_data": "UniTurnip0"}, {"text": ">>>", "callback_data": "UniTurnipFurther"}]]}, 'settings': ['number']}, {'title': 'A boolean', 'type': 'boolean', 'default': False, 'question': 'A boolean', 'main_type': 'object', 'required': True, 'last_key': 'fixedNoToolbar', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'Fixed array without buttons', 'keyboard': {"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, 'settings': ['boolean']}, {'title': 'A string', 'type': 'string', 'default': 'lorem ipsum', 'question': 'A string', 'main_type': 'object', 'required': False, 'last_key': 'fixedNoToolbar', 'last_object_data': {'main_type': 'object', 'required': []}, 'main_title': 'Fixed array without buttons', 'keyboard': 'with_skip', 'settings': 'without_skip'}])]

    State = State(Arrays)

    print('result', State.initialization())

    def next():
        print('result', State.next())

    while State.processing:
        next()
        input()

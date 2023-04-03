class State:
    def __init__(self, questions_list):
        self.current_state_num = [0]
        self.current_state_name = None
        self.questions_list = questions_list
        self.processing = None
        self.current_question = None
        self.last_question_key = None
        self.current_list_size = 0

    def initialization(self):
        self.processing = True
        current_question, self.current_state_num = get_question(self.questions_list)
        state_name = get_state_name(self.questions_list, self.current_state_num)
        return self.state_and_question_result(state_name, current_question)

    def next(self):
        self.current_state_num[-1] += 1
        return self.question()

    def last(self):
        self.current_state_num[-1] -= 1
        return self.question()

    def more_q__answer(self, move):
        return self.more_q_processing(move)

    def end(self):
        self.processing = False
        self.current_state_num = None
        return None, None

    def question(self):
        if self.current_main_q_in_list():
            question = get_current_question(self.questions_list, self.current_state_num)
            state_name = get_state_name(self.questions_list, self.current_state_num)
            if question == []:
                return self.end()
            elif type(question) == list:
                if self.last_question_key != state_name[-1] and self.last_question_key != 'more_q':
                    self.last_question_key = state_name[-1]
                    return self.state_and_question_result('more_q', '')
                self.last_question_key = state_name[-1]
                current_question, current_state_num = get_question(question)
                self.current_state_num += current_state_num
                return check_state_and_question(state_name, current_question)
            elif type(question) == tuple:
                if self.return_last_question_or_no(main=True):
                    if self.last_question_key != question[0] and self.last_question_key != 'more_q':
                        self.last_question_key = question[0]
                        return self.state_and_question_result('more_q', '')
                    self.last_question_key = question[0]
                if type(question[1]) == list:
                    current_question, current_state_num = get_question(question[1])
                    self.current_state_num += [1] + current_state_num
                    return self.state_and_question_result(state_name, current_question)
            return self.state_and_question_result(state_name, question)
        else:
            if self.return_last_question_or_no():
                self.current_state_num[-1] += 1
                self.last_question_key = 'more_q'
                return self.state_and_question_result('more_q', '')
            if len(self.current_state_num) == 1:
                if -1 > self.current_state_num[0] > len(self.questions_list):
                    return self.next()
                else:
                    return self.end()
            self.current_state_num = self.current_state_num[:-1]
            if type(self.current_state_num) == int:
                return self.end()
            self.current_state_num = self.current_state_num[:-1]
            self.current_state_num[-1] += 1
            return self.next()

    def more_q_processing(self, move=None):
        if move is None:
            return self.state_and_question_result('more_q', '')
        else:
            if move == 'UniTurnipMore':
                self.current_state_num = self.current_state_num[:-1]
                self.current_state_num[-1] -= 1
                return self.next()
            else:
                return self.next()

    def current_main_q_in_list(self, is_last_question=False):
        curr_main_q_num = self.current_state_num[-1]
        if is_last_question:
            questions_list = get_current_question(self.questions_list, self.current_state_num[:-1])
            self.current_list_size = len(questions_list)
            return curr_main_q_num == self.current_list_size
        if len(self.current_state_num) == 1:
            self.current_list_size = len(self.questions_list)
            return -1 < curr_main_q_num <= self.current_list_size
        questions_list = get_current_question(self.questions_list, self.current_state_num)
        self.current_list_size = len(questions_list)
        return -1 < curr_main_q_num <= self.current_list_size

    def return_last_question_or_no(self, main=False):
        if self.current_main_q_in_list(is_last_question=True) or main:
            question = get_current_question(self.questions_list, self.current_state_num[:-1])
            question = check_question(question)
            return question_type_is_array(question)
        return False

    def state_and_question_result(self, state, question):
        self.current_state_name = state
        if state == 'more_q':
            state_and_question = question__do_you_need_more_question_or_no()
        else:
            state_and_question = check_state_and_question(state, question)
        return state_and_question


def question__do_you_need_more_question_or_no():
    question = {
        'question': 'Do you need the last question again?',
        'type': 'more_q'}
    return ['more_q'], question


def question_type_is_array(question):
    if type(question) == dict:
        if 'type' in question.keys() and question['type'] == 'array':
            return True
        elif 'last_type' in question.keys() and question['last_type'] == 'array':
            return True
        elif 'last_object_data' in question.keys():
            return question_type_is_array(question['last_object_data'])
    return False


def tuple_unpack(tuple_schema):
    if type(tuple_schema) == dict:
        return '', tuple_schema
    if type(tuple_schema[0]) == str:
        if type(tuple_schema[1]) == dict:
            return tuple_schema
        else:
            raise TypeError(type(tuple_schema), tuple_schema)
    elif type(tuple_schema[0]) == tuple:
        return tuple_unpack(tuple_schema[0])
    else:
        raise TypeError(type(tuple_schema))


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


def get_state_name(question, num):
    if type(num) == list:
        if len(num) != 0:
            if len(question) <= num[0]:
                return []
            if type(question[num[0]]) == tuple:
                return [question[num[0]][0]] + get_state_name(question[num[0]], num[1:])
            else:
                return get_state_name(question[num[0]], num[1:])
    elif type(num) == int:
        if type(question[num]) == tuple:
            return [question[num][0]]
    return []


def check_state_and_question(state_name, question):
    if type(question) == dict:
        return state_name, question
    elif type(question) == tuple:
        state, question_res = check_state_and_question([], question[1])
        if question[0] not in state_name:
            state_name += [question[0]]
        if state and state not in state_name:
            state_name += state
        return state_name, question_res
    else:
        raise TypeError(type(question), question)


def check_question(question):
    if type(question) == tuple:
        return check_question(question[1])
    elif type(question) == list:
        return check_question(question[-1])
    elif type(question) == dict:
        return question
    else:
        raise TypeError(type(question), question)


if __name__ == '__main__':
    Simple = [('firstName', (None, ['string'])), ('lastName', (None, ['string'])), ('telephone', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])})]
    Nested = [('first', (None, ['string'])), ('tasks', [('title', (None, ['string'])), ('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])})])]
    Arrays = [('listOfStrings', {'type': 'string', 'default': 'bazinga', 'question': 'A list of strings', 'required': False, 'last_key': 'listOfStrings', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'A list of strings', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('multipleChoicesList', {'type': 'string', 'enum': ['foo', 'bar', 'fuzz', 'qux'], 'question': 'A multiple choices list', 'required': False, 'last_key': 'multipleChoicesList', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'A multiple choices list', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('fixedItemsList', [{'title': 'A string value', 'type': 'string', 'default': 'lorem ipsum', 'question': 'A string value', 'required': True, 'last_key': 'fixedItemsList', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'A list of fixed items', 'keyboard': None, 'settings': ['string']}, {'title': 'a boolean value', 'type': 'boolean', 'question': 'a boolean value', 'required': True, 'last_key': 'fixedItemsList', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'A list of fixed items', 'keyboard': {"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, 'settings': ['boolean']}, {'title': 'Additional item', 'type': 'number', 'question': 'Additional item', 'required': False, 'last_key': 'fixedItemsList', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'A list of fixed items', 'keyboard': 'with_skip', 'settings': 'without_skip'}]), ('minItemsList', [('name', {'type': 'string', 'default': 'Default name', 'question': 'A list with a minimal number of items', 'required': False, 'last_key': 'minItemsList', 'last_object_data': {'required': [], 'last_key': 'minItemsList', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'A list with a minimal number of items', 'minItems': 3}, 'last_type': 'object', 'keyboard': 'with_skip', 'settings': 'without_skip'})]), ('defaultsAndMinItems', {'type': 'string', 'default': 'unidentified', 'question': 'List and item level defaults', 'required': False, 'last_key': 'defaultsAndMinItems', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'List and item level defaults', 'minItems': 5, 'keyboard': None, 'settings': ['string']}), ('nestedList', {'type': 'string', 'default': 'lorem ipsum', 'question': 'Inner list', 'required': False, 'last_key': 'nestedList', 'last_object_data': {'required': [], 'last_key': 'nestedList', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'Nested list'}, 'last_type': 'array', 'main_title': 'Inner list', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('unorderable', {'type': 'string', 'default': 'lorem ipsum', 'question': 'Unorderable items', 'required': False, 'last_key': 'unorderable', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'Unorderable items', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('unremovable', {'type': 'string', 'default': 'lorem ipsum', 'question': 'Unremovable items', 'required': False, 'last_key': 'unremovable', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'Unremovable items', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('noToolbar', {'type': 'string', 'default': 'lorem ipsum', 'question': 'No add, remove and order buttons', 'required': False, 'last_key': 'noToolbar', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'No add, remove and order buttons', 'keyboard': 'with_skip', 'settings': 'without_skip'}), ('fixedNoToolbar', [{'title': 'A number', 'type': 'number', 'default': 42, 'question': 'A number', 'required': True, 'last_key': 'fixedNoToolbar', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'Fixed array without buttons', 'keyboard': {"inline_keyboard": [[{"text": "1", "callback_data": "UniTurnip1"}, {"text": "2", "callback_data": "UniTurnip2"}, {"text": "3", "callback_data": "UniTurnip3"}], [{"text": "4", "callback_data": "UniTurnip4"}, {"text": "5", "callback_data": "UniTurnip5"}, {"text": "6", "callback_data": "UniTurnip6"}], [{"text": "7", "callback_data": "UniTurnip7"}, {"text": "8", "callback_data": "UniTurnip8"}, {"text": "9", "callback_data": "UniTurnip9"}], [{"text": "C", "callback_data": "UniTurnipClear"}, {"text": "0", "callback_data": "UniTurnip0"}, {"text": ">>>", "callback_data": "UniTurnipFurther"}]]}, 'settings': ['number']}, {'title': 'A boolean', 'type': 'boolean', 'default': False, 'question': 'A boolean', 'required': True, 'last_key': 'fixedNoToolbar', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'Fixed array without buttons', 'keyboard': {"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, 'settings': ['boolean']}, {'title': 'A string', 'type': 'string', 'default': 'lorem ipsum', 'question': 'A string', 'required': False, 'last_key': 'fixedNoToolbar', 'last_object_data': {'required': [], 'last_key': None, 'last_object_data': None, 'last_type': 'object'}, 'last_type': 'array', 'main_title': 'Fixed array without buttons', 'keyboard': 'with_skip', 'settings': 'without_skip'}])]

    State = State(Arrays)

    print('result', State.initialization())

    def next():
        print('result', State.next())

    while State.processing:
        next()
        input()

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
            self.current_state_num = self.current_state_num[:-1][-1]
            if type(self.current_state_num) == int:
                return self.end()
            return self.next()

    def end(self):
        self.processing = False
        self.current_state_num = None
        return None

    def current_main_q_in_list(self):
        curr_main_q_num = self.current_state_num[-1]
        questions_list = get_current_question(self.questions_list, self.current_state_num)
        return -1 < curr_main_q_num <= len(questions_list)


def get_question(questions):
    print(questions)
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
    Simple = ([('firstName', (None, ['string'])), ('lastName', (None, ['string'])), ('telephone', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])})], {'firstName': None, 'lastName': None, 'telephone': None})
    Nested = [('first', (None, ['string'])), ('tasks', [('title', (None, ['string'])), ('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])})])]
    Arrays = [('listOfStrings', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('multipleChoicesList', {'with_skip': ({"inline_keyboard": [[{"text": "foo", "callback_data": "UniTurnip_foo"}, {"text": "bar", "callback_data": "UniTurnip_bar"}, {"text": "fuzz", "callback_data": "UniTurnip_fuzz"}, {"text": "qux", "callback_data": "UniTurnip_qux"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string', 'custom']), 'without_skip': ({"inline_keyboard": [[{"text": "foo", "callback_data": "UniTurnip_foo"}, {"text": "bar", "callback_data": "UniTurnip_bar"}, {"text": "fuzz", "callback_data": "UniTurnip_fuzz"}, {"text": "qux", "callback_data": "UniTurnip_qux"}]]}, ['string', 'custom'])}), ('fixedItemsList', [(None, ['string']), ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean']), {'with_skip': ({"inline_keyboard": [[{"text": "1", "callback_data": "UniTurnip1"}, {"text": "2", "callback_data": "UniTurnip2"}, {"text": "3", "callback_data": "UniTurnip3"}], [{"text": "4", "callback_data": "UniTurnip4"}, {"text": "5", "callback_data": "UniTurnip5"}, {"text": "6", "callback_data": "UniTurnip6"}], [{"text": "7", "callback_data": "UniTurnip7"}, {"text": "8", "callback_data": "UniTurnip8"}, {"text": "9", "callback_data": "UniTurnip9"}], [{"text": "C", "callback_data": "UniTurnipClear"}, {"text": "0", "callback_data": "UniTurnip0"}, {"text": ">>>", "callback_data": "UniTurnipFurther"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['number']), 'without_skip': ({"inline_keyboard": [[{"text": "1", "callback_data": "UniTurnip1"}, {"text": "2", "callback_data": "UniTurnip2"}, {"text": "3", "callback_data": "UniTurnip3"}], [{"text": "4", "callback_data": "UniTurnip4"}, {"text": "5", "callback_data": "UniTurnip5"}, {"text": "6", "callback_data": "UniTurnip6"}], [{"text": "7", "callback_data": "UniTurnip7"}, {"text": "8", "callback_data": "UniTurnip8"}, {"text": "9", "callback_data": "UniTurnip9"}], [{"text": "C", "callback_data": "UniTurnipClear"}, {"text": "0", "callback_data": "UniTurnip0"}, {"text": ">>>", "callback_data": "UniTurnipFurther"}]]}, ['number'])}]), ('minItemsList', [('name', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])})]), ('defaultsAndMinItems', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('nestedList', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('unorderable', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('unremovable', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('noToolbar', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('fixedNoToolbar', [({"inline_keyboard": [[{"text": "1", "callback_data": "UniTurnip1"}, {"text": "2", "callback_data": "UniTurnip2"}, {"text": "3", "callback_data": "UniTurnip3"}], [{"text": "4", "callback_data": "UniTurnip4"}, {"text": "5", "callback_data": "UniTurnip5"}, {"text": "6", "callback_data": "UniTurnip6"}], [{"text": "7", "callback_data": "UniTurnip7"}, {"text": "8", "callback_data": "UniTurnip8"}, {"text": "9", "callback_data": "UniTurnip9"}], [{"text": "C", "callback_data": "UniTurnipClear"}, {"text": "0", "callback_data": "UniTurnip0"}, {"text": ">>>", "callback_data": "UniTurnipFurther"}]]}, ['number']), ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean']), {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}])]


    State = State(Arrays)

    print('result', State.initialization())

    def next():
        print('result', State.next())

    while State.processing:
        next()
        input()

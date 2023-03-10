import sys

from UniTurnip_for_bots.handlers.read_the_schema import SchemaRead
from UniTurnip_for_bots.handlers.tools import read_schema
from UniTurnip_for_bots.handlers.constants import DEFAULT_SCHEME
from UniTurnip_for_bots.handlers.state import State


class UniTurnip:
    def __init__(self):
        # non-changing during the survey
        self.scheme_not_definite = True
        self.questions_list = []

        # current
        self.State = None
        self.current_state_name = None

        # for bot use
        self.processing = False
        self.freeze = False
        self.current_question = None

        # stores user responses
        self.user_answers = {}

    def read_json(self, schema: str | dict):
        '''
        Создает опрос на основе переданной ему json схемы
        :param schema: Сюда передается json схема
        :return: Данная функция нечего не возвращает, но с ее помощью в памяти сохраняются настройки для создания опроса
        '''
        schema = read_schema(schema)
        Schema = SchemaRead(schema)
        self.questions_list, self.user_answers = Schema.get()
        self.State = State(self.questions_list)
        self.scheme_not_definite = False
        print('===========| question_list |===========')
        for value in self.questions_list:
            if list(value[1].keys())[0] == 0:
                print(value[0])
                for key, value in value[1].items():
                    print(f'{key} --- {value}')
            else:
                print(value)
        print('============| user_answers |===========')
        print(self.user_answers)
        print('=======================================')

    def start_survey(self):
        '''
        При вызове функции начнется опрос и в переменных: "self.current_question" и "self.current_keyboard", появится
        первый вопрос и клавиатура прилагаемая к этому вопросу
        '''
        if self.scheme_not_definite:
            self.read_json(DEFAULT_SCHEME)
        self.current_question = self.State.initialization()
        print()
        print('=============| settings |=============')
        print(self.current_state_num)
        print(self.current_state_name)
        print(self.user_answers)
        print('=============| current_questions |=============')
        print(self.current_question)
        for key, value in self.current_question.items():
            print(f'{key} --- {value}')
        print('===============================================')

    def next(self):
        """
        Задать следующий вопрос
        """
        self.initialization(+1)

        if self.current_question:
            print()
            print('=============| settings |=============')
            print(self.current_state_num)
            print(self.current_state_name)
            print(self.user_answers)
            print('=============| current_questions |=============')
            print(self.current_question)
            for key, value in self.current_question.items():
                print(f'{key} --- {value}')
            print('===============================================')

    def back(self):
        """
        Вернутся к прошлому вопросу
        """
        print('back ---------------')
        self.initialization(-1)

    def end_survey(self):
        self.current_state_name = None
        self.current_state_num = None
        self.current_question = None
        self.questions_list = None
        self.scheme_not_definite = True
        self.processing = False
        # self.user_answers = self.clear_answers(self.user_answers)

    def answer(self, user_answer):
        """
        Принимает ответы на вопросы от пользователя
        :param user_answer:
        :return:
        """
        if user_answer.startswith('UniTurnip'):
            self.button_response_processing(user_answer)
        elif 'string' in self.current_question['keyboard_settings']\
                or 'number' in self.current_question['keyboard_settings']:
            self.string_response_processing(user_answer)
        else:
            self.back()

    def get_new_question(self):
        pass

    def string_response_processing(self, answer):
        if self.current_question['type'] == 'string':
            if 'minLength' in self.current_question.keys():
                min_len = int(self.current_question['minLength'])
                if len(answer) < min_len:
                    self.back()
                else:
                    self.save_and_next(answer)
            else:
                self.save_and_next(answer)
        elif self.current_question['type'] == 'array':
            self.save_and_next(answer)
        elif self.current_question['type'] == 'number':
            self.save_and_next(answer)

    def button_response_processing(self, button):
        if button == 'UniTurnipCancel' and 'cancel' in self.current_question['keyboard_settings']:
            self.next()
        elif button in ('UniTurnipMore', 'UniTurnipNotMore') and 'more' in self.current_question['keyboard_settings']:
            if button == 'UniTurnipNotMore':
                self.initialization(-1, work_with_add_q=True)
            else:
                self.initialization(0, work_with_add_q=True)
        elif button in ('UniTurnipTrue', 'UniTurnipFalse') and 'boolean' in self.current_question['keyboard_settings']:
            answer = True if button == 'UniTurnipTrue' else False
            self.save_and_next(answer)
        elif 'custom' in self.current_question['keyboard_settings']:
            answer = button.strip('UniTurnip_')
            self.save_and_next(answer)

    def save_and_next(self, answer):
        self.user_answers = self.user_answers_save(answer, self.user_answers)
        if self.check_additional_param():
            self.next()

    def check_additional_param(self):
        if 'minItems' in self.current_question.keys():
            if self.current_question['minItems'] >= self.current_state_num[2] + 2:
                return self.initialization(0, work_with_add_q=True)
            else:
                return self.initialization(0, ask__giv_more_q=True)
        return True

    def user_answers_save(self, answer, all_user_answers):
        answers_cope = dict(all_user_answers)
        for key in answers_cope.keys():
            if type(self.current_state_name) == str:
                if key == self.current_state_name:
                    if type(all_user_answers) is None:
                        all_user_answers = self.save_answer(all_user_answers, key, answer)
                        return all_user_answers
                    elif type(all_user_answers[key]) == list:
                        all_user_answers[key] = self.save_answer(all_user_answers[key], key, answer)
                        return all_user_answers
            else:
                if key == self.current_state_name[0]:
                    all_user_answers[key] = self.save_answer(all_user_answers[key], self.current_state_name[1], answer)
                    return all_user_answers
        raise KeyError(self.user_answers, self.current_state_name)

    def save_answer(self, user_answers, key, answer):
        if type(user_answers) == list:
            if len(user_answers) == 0 or type(user_answers[0]) != dict:
                user_answers += [answer]
            elif self.current_state_num[2] == 0 and len(user_answers) != 0:
                user_answers[0][key] = answer
            elif len(user_answers) == 0:
                user_answers = [{key: answer}]
            else:
                if self.current_state_num[2] >= len(user_answers):
                    user_answers += [{key: answer}]
                else:
                    user_answers[self.current_state_num[2]][key] = answer
        elif type(user_answers) == dict:
            user_answers[key] = answer
        return user_answers

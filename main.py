from UniTurnip_for_bots.handlers.read_the_schema import SchemaRead
from UniTurnip_for_bots.handlers.tools.work_with_schema import read_schema
from UniTurnip_for_bots.handlers.constants import DEFAULT_SCHEME
from UniTurnip_for_bots.handlers.state import State
from for_info.printing_data_in_terminal import Printing
from UniTurnip_for_bots.handlers.tools.string_response_processing import StringResponseProcessing
from UniTurnip_for_bots.handlers.tools.button_response_processing import ButtonResponsePrecessing
from UniTurnip_for_bots.handlers.tools.save_user_answer import UserAnswerSave


class UniTurnip:
    def __init__(self):
        # non-changing during the survey
        self.scheme_not_definite = True
        self.questions_list = []
        self.current_state_name = None
        self.current_list_size = 0

        # other classes
        self.State = None
        dict_with_func = {
            'save_and_next': self.save_and_next,
            'next': self.next,
            'back': self.back
        }
        self.StringResponse = StringResponseProcessing(dict_with_func)
        self.ButtonResponse = ButtonResponsePrecessing(dict_with_func)
        self.SaveUserAnswer = UserAnswerSave(dict_with_func)

        # for bot use
        self.processing = False
        self.freeze = False
        self.current_question = None

        # stores user responses
        self.all_user_answers = {}

    def read_json(self, schema: str | dict):
        '''
        Создает опрос на основе переданной ему json схемы
        :param schema: Сюда передается json схема
        :return: Данная функция нечего не возвращает, но с ее помощью в памяти сохраняются настройки для создания опроса
        '''
        schema = read_schema(schema)
        Schema = SchemaRead(schema)
        self.questions_list, self.all_user_answers = Schema.get()
        self.State = State(self.questions_list)
        self.scheme_not_definite = False
        print('===========| question_list |===========')
        Printing().in_terminal(self.questions_list)
        print('============| user_answers |===========')
        print(self.all_user_answers)
        print('=======================================')

    def start_survey(self):
        '''
        При вызове функции начнется опрос и в переменных: "self.current_question" и "self.current_keyboard", появится
        первый вопрос и клавиатура прилагаемая к этому вопросу
        '''
        if self.scheme_not_definite:
            self.read_json(DEFAULT_SCHEME)
        self.processing = True
        self.move('init')

    def next(self):
        """
        Задать следующий вопрос
        """
        self.move('next')

    def back(self):
        """
        Вернутся к прошлому вопросу
        """
        print('back ---------------')
        self.move('back')

    def end_survey(self):
        self.State.current_state_num = None
        self.current_question = None
        self.questions_list = None
        self.scheme_not_definite = True
        self.processing = False
        self.all_user_answers = None

    def answer(self, user_answer):
        """
        Принимает ответы на вопросы от пользователя
        :param user_answer:
        :return:
        """
        if user_answer.startswith('UniTurnip'):
            self.ButtonResponse.processing(user_answer, self.current_question)
        elif 'string' in self.current_question['keyboard_settings']\
                or 'number' in self.current_question['keyboard_settings']:
            self.StringResponse.processing(user_answer, self.current_question)
        else:
            self.back()

    def save_and_next(self, answer):
        self.SaveUserAnswer.save(answer, self.all_user_answers, self.current_state_name, self.State.current_list_size)
        self.next()

    # ===========================================================================
    # ===========================================================================
    # ===========================================================================
    def move(self, key):
        all_moves = {
            'init': self.State.initialization,
            'next': self.State.next,
            'back': self.State.last
        }
        self.current_state_name, self.current_question = all_moves[key]()
        self.current_list_size = self.State.current_list_size
        if self.State.processing:
            self.keyboard_check()
            print()
            print('=============| settings |=============')
            print(self.State.current_state_num)
            print(self.all_user_answers)
            print('=============| current_questions |=============')
            print(self.current_question)
            Printing().in_terminal(self.current_question)
            print('===============================================')

    def keyboard_check(self):
        if self.current_question['keyboard_settings'] == 'choice_skip_or_no':
            keyboard = self.current_question['keyboard']
            if 'minItems' in self.current_question.keys():
                if type(self.current_question['minItems']) == int:
                    self.current_question['minItems'] = {
                        'len': self.current_question['minItems'],
                        'cur': 0
                    }
                min_length = self.current_question['minItems']
                if min_length['len'] >= min_length['cur']:
                    self.current_question['keyboard'] = keyboard['without_skip'][0]
                    self.current_question['keyboard_settings'] = keyboard['without_skip'][1]
                else:
                    self.current_question['keyboard'] = keyboard['keyboard']['with_skip'][0]
                    self.current_question['keyboard_settings'] = keyboard['keyboard']['with_skip'][1]
            else:
                self.current_question['keyboard'] = keyboard['with_skip'][0]
                self.current_question['keyboard_settings'] = keyboard['with_skip'][1]

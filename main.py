from UniTurnip_for_bots.handlers.keyboards import optional_questions  #, optional_callback_data
from UniTurnip_for_bots.handlers.tools import read_schema
from UniTurnip_for_bots.handlers.constants import DEFAULT_SCHEME
# from UniTurnip_for_bots.handlers.filters import Filter


class UniTurnip:
    def __init__(self):
        # non-changing during the survey
        self.required = []
        self.questions_keys = []
        self.properties = None
        self.scheme_not_definite = True
        # current
        self.current_state_num = None
        self.current_state_name = None
        self.current_question_settings = None
        # for bot use
        self.processing = False
        self.current_question = None
        self.current_keyboard = None
        # self.current_callback_data = ['non']
        # stores user responses
        self.user_answers = {}

        # self.Filter = Filter(self.current_callback_data)

    def read_json(self, schema: str | dict):
        '''
        Создает опрос на основе переданной ему json схемы
        :param schema: Сюда передается json схема
        :return: Данная функция нечего не возвращает, но с ее помощью в памяти сохраняются настройки для создания опроса
        '''
        schema = read_schema(schema)
        self.get_parameters_from_schema(schema)
        self.scheme_not_definite = False

    def start_survey(self):
        '''
        При вызове функции начнется опрос и в переменных: "self.current_question" и "self.current_keyboard", появится
        первый вопрос и клавиатура прилагаемая к этому вопросу
        '''
        if self.scheme_not_definite:
            self.read_json(DEFAULT_SCHEME)
        self.current_state_num = 1
        self.processing = True
        self.initialization()

    def next(self):
        """
        Задать следующий вопрос
        """
        self.current_state_num += 1
        self.initialization()

    def back(self):
        """
        Вернутся к прошлому вопросу
        """
        self.current_state_num -= 1
        self.initialization()

    def answer(self, user_answer):
        """
        Принимает ответы на вопросы от пользователя
        :param user_answer:
        :return:
        """
        answer_info = self.response_processing(user_answer)
        if answer_info is True:
            self.user_answers[self.current_state_name] = user_answer
        elif answer_info is False:
            self.back()
        elif answer_info == 'cancel':
            pass

    def initialization(self):
        if -1 < self.current_state_num <= len(self.questions_keys):
            self.current_state_name = self.questions_keys[self.current_state_num-1]
            self.create_current_questions()
        else:
            self.processing = False
            self.current_state_name = None

    def create_current_questions(self):
        # question
        self.current_question_settings = self.properties[self.current_state_name]
        self.current_question = self.current_question_settings['title']
        # keyboard
        if self.current_state_name not in self.required:
            self.current_keyboard = optional_questions
            # self.current_callback_data = optional_callback_data
            # self.Filter.callback_data = optional_callback_data
        else:
            # self.current_callback_data = ['non']
            # self.Filter.callback_data = self.current_callback_data
            self.current_keyboard = None

    def get_parameters_from_schema(self, schema: dict):
        if 'required' in schema:
            self.required = schema['required']
            if 'properties' in schema:
                self.properties = schema['properties']
                key_list = list(self.properties.keys())
                additional = [key for key in key_list if key not in self.required]
                self.questions_keys = tuple(self.required + additional)

    def response_processing(self, answer):
        if self.current_question_settings['type'] == 'string':
            if 'minLength' in self.current_question_settings:
                min_len = int(self.current_question_settings['minLength'])
                if len(answer) < min_len:
                    return False
            elif self.current_keyboard:
                if answer == 'cancel':
                    return 'cancel'
            return True
        else:
            return False

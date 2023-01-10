from UniTurnip_for_bots.handlers.read_the_schema import SchemaRead
from UniTurnip_for_bots.handlers.tools import read_schema
from UniTurnip_for_bots.handlers.constants import DEFAULT_SCHEME


class UniTurnip:
    def __init__(self):
        # non-changing during the survey
        self.scheme_not_definite = True
        self.questions_list = []

        # current
        self.current_state_num = None
        self.current_repetition_num = 0
        self.current_state_name = None
        self.current_array = None

        # for bot use
        self.processing = False
        self.current_question = None

        # stores user responses
        self.user_answers = {}

        self.last_type = None
        self.last_required = []
        self.last_key = None

        self.Read = SchemaRead()

    def read_json(self, schema: str | dict):
        '''
        Создает опрос на основе переданной ему json схемы
        :param schema: Сюда передается json схема
        :return: Данная функция нечего не возвращает, но с ее помощью в памяти сохраняются настройки для создания опроса
        '''
        schema = read_schema(schema)
        self.Read.schema_read(schema)
        self.questions_list = self.Read.questions_list
        self.user_answers = self.Read.response_stencil(schema)
        self.scheme_not_definite = False

    def start_survey(self):
        '''
        При вызове функции начнется опрос и в переменных: "self.current_question" и "self.current_keyboard", появится
        первый вопрос и клавиатура прилагаемая к этому вопросу
        '''
        if self.scheme_not_definite:
            self.read_json(DEFAULT_SCHEME)
        self.processing = True
        self.initialization(0)

    def next(self):
        """
        Задать следующий вопрос
        """
        self.initialization(+1)

    def back(self):
        """
        Вернутся к прошлому вопросу
        """
        self.initialization(-1)

    def answer(self, user_answer):
        """
        Принимает ответы на вопросы от пользователя
        :param user_answer:
        :return:
        """
        if user_answer.startswith('UniTurnip'):
            self.button_response_processing(user_answer)
        else:
            self.string_response_processing(user_answer)

    def initialization(self, num):
        if not self.current_state_num:
            self.current_state_num = [num, -1]
        if -1 < self.current_state_num[0] < len(self.questions_list):
            if self.current_state_num[1] == -1:
                self.current_state_num[0] = self.current_state_num[0] + num
            else:
                self.current_state_num[1] = self.current_state_num[1] + num

            if self.current_state_num[1] == -1 and 'type' not in self.questions_list[self.current_state_num[0]][1].keys():
                self.current_state_num[1] = 0
                self.current_array = self.questions_list[self.current_state_num[0]]
                self.current_question = self.current_array[1][self.current_state_num[1]][1]
                self.current_state_name = self.current_array[1][self.current_state_num[1]][0]
                return
            elif self.current_state_num[1] != -1 and -1 < self.current_state_num[1] <= max(self.current_array[1].keys()):
                self.current_question = self.current_array[1][self.current_state_num[1]][1]
                self.current_state_name = self.current_array[1][self.current_state_num[1]][0]
                return
            elif self.current_state_num[1] != -1 and -1 < self.current_state_num[1] > max(self.current_array[1].keys()):
                self.current_state_num[1] = -1
                self.current_state_num[0] += 1
                self.current_repetition_num = 0

            if self.current_state_num[1] == -1 and -1 < self.current_state_num[0] < len(self.questions_list):
                self.current_state_name = self.questions_list[self.current_state_num[0]][0]
                self.current_question = self.questions_list[self.current_state_num[0]][1]
            else:
                self.current_state_num = None
                self.processing = False
        else:
            self.current_state_num = None
            self.processing = False
            return

    def string_response_processing(self, answer):
        if self.current_question['type'] == 'string':
            if 'minLength' in self.current_question['answer_settings']:
                min_len = int(self.current_question['answer_settings']['minLength'])
                if len(answer) < min_len:
                    self.back()
                else:
                    self.user_answers = self.user_answers_save(answer, self.user_answers)
            else:
                self.user_answers = self.user_answers_save(answer, self.user_answers)
        elif self.current_question['type'] == 'array':
            self.user_answers = self.user_answers_save(answer, self.user_answers)

    def button_response_processing(self, button):
        if button == 'UniTurnipCancel' and 'cancel' in self.current_question['keyboard_settings']:
            return
        elif button in ('UniTurnipMore', 'UniTurnipNotMore') and 'more' in self.current_question['keyboard_settings']:
            if 'NotMore' not in button:
                self.current_state_num[1] = -1
                self.back()
                self.current_repetition_num += 1
        elif button in ('UniTurnipTrue', 'UniTurnipFalse') and 'boolean' in self.current_question['keyboard_settings']:
            self.user_answers = self.user_answers_save(bool(button.strip('UniTurnip_')), self.user_answers)

    def user_answers_save(self, answer, all_user_answers):
        answers_cope = dict(all_user_answers)
        for key in answers_cope.keys():
            if self.current_question['last_key'] is None:
                if key == self.current_state_name:
                    all_user_answers = self.save_answer(all_user_answers, key, answer)
                    return all_user_answers
            else:
                if key == self.current_question['last_key']:
                    all_user_answers[key] = self.save_answer(all_user_answers[key], self.current_state_name, answer)
                    return all_user_answers
        raise KeyError(self.current_state_name, self.current_question['last_key'])

    def save_answer(self, user_answers, key, answer):
        if type(user_answers) == list:
            if self.current_repetition_num == 0:
                user_answers[0][key] = answer
            else:
                if self.current_repetition_num >= len(user_answers):
                    user_answers += [{key: answer}]
                else:
                    user_answers[self.current_repetition_num][key] = answer
        elif type(user_answers) == dict:
            user_answers[key] = answer
        return user_answers

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

        # for bot use
        self.processing = False
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
        Schema = SchemaRead()
        Schema.schema_read(schema)
        self.questions_list = Schema.questions_list
        self.user_answers = Schema.response_stencil(schema)
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

    def end_survey(self):
        self.current_state_name = None
        self.current_state_num = None
        self.current_question = None
        self.questions_list = None
        self.scheme_not_definite = True
        self.processing = False

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
            self.current_state_num = [num, -1]  # [main question, additional questions]
        elif self.current_state_num[1] != -1 or -1 < self.current_state_num[0]+1 < len(self.questions_list) or num < 0:
            if self.current_state_num[1] == -1:
                self.current_state_num[0] = self.current_state_num[0] + num
            else:
                self.current_state_num[1] = self.current_state_num[1] + num
        else:
            return self.end_survey()

        curr_main_q_num, curr_add_q_num = self.current_state_num[:2]
        q_name, q_data = self.questions_list[curr_main_q_num]

        if 'type' not in q_data.keys():  # additional question processing
            if curr_add_q_num == -1:  # if the stage num of the additional question is not specified
                add_q_name, add_q_info = q_data[0]
                self.current_state_num = [curr_main_q_num, 0, 0]
                self.current_question = add_q_info
                self.current_state_name = [q_name, add_q_name]
                return
            elif self.current_state_num[1] != -1:
                if -1 < curr_add_q_num <= max(q_data.keys()):  # if additional questions
                    add_q_name, add_q_info = q_data[curr_add_q_num]
                    self.current_question = add_q_info
                    self.current_state_name = [q_name, add_q_name]
                    return
                else:  # if additional questions are over
                    self.current_state_num = [curr_main_q_num + 1, -1]

        if curr_add_q_num == -1 and -1 < curr_main_q_num < len(self.questions_list):
            self.current_state_name = q_name
            self.current_question = q_data
        else:
            self.end_survey()

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
                self.current_repetition_num += 1
                self.back()
        elif button in ('UniTurnipTrue', 'UniTurnipFalse') and 'boolean' in self.current_question['keyboard_settings']:
            answer = True if button == 'UniTurnipTrue' else False
            self.user_answers = self.user_answers_save(answer, self.user_answers)

    def user_answers_save(self, answer, all_user_answers):
        answers_cope = dict(all_user_answers)
        for key in answers_cope.keys():
            if type(self.current_state_name) == str:
                if key == self.current_state_name:
                    all_user_answers = self.save_answer(all_user_answers, key, answer)
                    return all_user_answers
            else:
                if key == self.current_state_name[0]:
                    all_user_answers[key] = self.save_answer(all_user_answers[key], self.current_state_name[1], answer)
                    return all_user_answers
        raise KeyError(self.user_answers, self.current_state_name)

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

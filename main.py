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
        Schema = SchemaRead(schema)
        self.questions_list, self.user_answers = Schema.get()
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
        self.processing = True
        self.initialization(0)

    def next(self):
        """
        Задать следующий вопрос
        """
        self.initialization(+1)

        if self.current_question:
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
        elif 'string' in self.current_question['keyboard_settings']:
            self.string_response_processing(user_answer)
        else:
            self.back()

    def initialization(self, num, work_with_add_q=False):
        # =======|  determination of the current state number |=======
        if work_with_add_q:
            if num == 0:
                self.current_state_num[0] -= 1
                self.current_state_num[1] = -1
                self.current_state_num[2] += 1
            elif num == -1:
                if -1 < self.current_state_num[0] < len(self.questions_list):
                    self.current_state_num = [self.current_state_num[0], -1]
                else:
                    return self.end_survey()
            return
        elif not self.current_state_num:
            self.current_state_num = [num, -1]  # [main question, additional questions]
        elif self.current_state_num[1] != -1 or -1 < self.current_state_num[0]+1 < len(self.questions_list) or num < 0:
            if self.current_state_num[1] == -1:
                self.current_state_num[0] += num
            else:
                self.current_state_num[1] += num
        else:
            return self.end_survey()
        # ============================================================

        # ===============| cut of variable names |===============
        curr_main_q_num, curr_add_q_num = self.current_state_num[:2]
        q_name, q_data = self.questions_list[curr_main_q_num]
        # =======================================================

        # =====================| functions |=====================
        def set_new_main_question():
            add_q_name, add_q_info = q_data[0]
            if len(self.current_state_num) == 2:
                self.current_state_num = [curr_main_q_num, 0, 0]
            self.current_state_num = [curr_main_q_num, 0, self.current_state_num[2]]
            self.current_question = add_q_info
            self.current_state_name = [q_name, add_q_name]

        def set_first_additional_question():
            add_q_name, add_q_info = q_data[curr_add_q_num]
            self.current_question = add_q_info
            self.current_state_name = [q_name, add_q_name]

        def next_main_question():
            if curr_add_q_num == -1 and -1 < curr_main_q_num < len(self.questions_list):
                self.current_state_name = q_name
                self.current_question = q_data
            else:
                self.end_survey()
        # =======================================================

        # ========| set new current question (main or add) |========
        if 'type' not in q_data.keys():  # additional question processing
            if curr_add_q_num == -1:  # if the stage num of the additional question is not specified
                set_new_main_question()
            elif self.current_state_num[1] != -1:
                if -1 < curr_add_q_num <= max(q_data.keys()):  # if additional questions
                    set_first_additional_question()
                else:  # if additional questions are over
                    if self.current_state_num[0] == 0:  # if current add questions is first main questions
                        self.current_state_num = [curr_main_q_num, -1]
                        set_new_main_question()
                    else:
                        # set next add question
                        self.current_state_num = [curr_main_q_num, -1]
                        next_main_question()
        else:
            next_main_question()
        # ==========================================================

    def string_response_processing(self, answer):
        if self.current_question['type'] == 'string':
            if 'minLength' in self.current_question.keys():
                min_len = int(self.current_question['minLength'])
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
            if button == 'UniTurnipNotMore':
                self.initialization(-1, work_with_add_q=True)
            else:
                self.initialization(0, work_with_add_q=True)
        elif button in ('UniTurnipTrue', 'UniTurnipFalse') and 'boolean' in self.current_question['keyboard_settings']:
            answer = True if button == 'UniTurnipTrue' else False
            self.user_answers = self.user_answers_save(answer, self.user_answers)
        elif 'custom' in self.current_question['keyboard_settings']:
            answer = button.strip('UniTurnip_')
            self.user_answers = self.user_answers_save(answer, self.user_answers)
        else:
            raise KeyError(button)

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

    # def clear_answers(self, answers):
    #     if type(answers) == dict:
    #         answers_cope = dict(answers)
    #         for key, value in answers_cope.items():
    #             if value is None:
    #                 answers.pop(key)
    #             elif type(value) in (list, dict):
    #                 self.clear_answers(value)
    #         return answers
    #     elif type(answers) == list:
    #         result_answers = []
    #         for value in answers:
    #             result_answers += self.clear_answers(value)
    #         return result_answers

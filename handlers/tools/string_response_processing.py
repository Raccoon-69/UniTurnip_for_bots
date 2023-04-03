class StringResponseProcessing:
    def __init__(self, dict_with_func_from_main):
        self.dict_with_func_from_main = dict_with_func_from_main
        self.current_question = None
        self.user_answer = None

    def processing(self, answer, current_question):
        self.user_answer = answer
        self.current_question = current_question
        if current_question['type'] == 'string':
            self.min_length()
        elif current_question['type'] == 'array':
            self.dict_with_func_from_main['save_and_next'](answer)
        elif current_question['type'] == 'number':
            self.dict_with_func_from_main['save_and_next'](answer)

    def min_length(self):
        if 'minLength' in self.current_question.keys():
            min_len = int(self.current_question['minLength']['len'])
            if len(self.user_answer) < min_len:
                self.dict_with_func_from_main['back']()
            else:
                self.dict_with_func_from_main['save_and_next'](self.user_answer)
        else:
            self.dict_with_func_from_main['save_and_next'](self.user_answer)

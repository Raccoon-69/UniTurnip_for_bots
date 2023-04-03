class UserAnswerSave:
    def __init__(self, dict_with_func_from_main):
        self.dict_with_func_from_main = dict_with_func_from_main

    def save(self, answer, all_user_answers, current_state_name, current_list_size):
        all_answers_cope = dict(all_user_answers)
        for key in all_answers_cope.keys():
            if len(current_state_name) == 1:
                if key == current_state_name[0]:
                    if all_user_answers[key] is None:
                        all_user_answers = self.save_answer(all_user_answers, key, answer, current_list_size)
                        return all_user_answers
                    elif type(all_user_answers[key]) == list:
                        all_user_answers[key] = self.save_answer(all_user_answers[key], key, answer, current_list_size)
                        return all_user_answers
            else:
                pass
        raise KeyError(current_state_name, answer, all_user_answers)

    def save_answer(self, all_user_answers, key, answer, current_list_size):
        if type(all_user_answers) == list:
            if len(all_user_answers) == 0 or type(all_user_answers[0]) != dict:
                all_user_answers += [answer]
            elif current_list_size == 0 and len(all_user_answers) != 0:
                all_user_answers[0][key] = answer
            elif len(all_user_answers) == 0:
                all_user_answers = [{key: answer}]
            else:
                if current_list_size >= len(all_user_answers):
                    all_user_answers += [{key: answer}]
                else:
                    all_user_answers[current_list_size][key] = answer
        elif type(all_user_answers) == dict:
            all_user_answers[key] = answer
        return all_user_answers

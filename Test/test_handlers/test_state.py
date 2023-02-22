from unittest import TestCase, main
from UniTurnip_for_bots.handlers.state import State, get_question, get_current_question


class TestInlineKeyboardsFile(TestCase):
    def test_get_current_question(self):
        questions = ['test', ['question', 'test']]
        num = [1, 0]
        self.assertEqual(get_current_question(questions, num), 'question')
        questions = ['test', ['test', [['test', 'test', ['question', 'test'], 'test'], 'test', 'test'], 'test'], 'test']
        num = [1, 1, 0, 2, 0]
        self.assertEqual(get_current_question(questions, num), 'question')
        questions = ['question', ['test', [['test', 'test', ['test', 'test'], 'test'], 'test', 'test'], 'test'], 'test']
        num = 0
        self.assertEqual(get_current_question(questions, num), 'question')

        question_list = [('first', (None, ['string'])), ('tasks', [('title', (None, ['string'])), ('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])})])]
        num = [0]
        self.assertEqual(get_current_question(question_list, num), ('first', (None, ['string'])))
        question_list = [('first', (None, ['string'])), ('tasks', [('title', (None, ['string'])), ('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])})])]
        num = [1]
        self.assertEqual(get_current_question(question_list, num), question_list[1])
        question_list = [('first', (None, ['string'])), ('tasks', [('title', (None, ['string'])), ('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])})])]
        num = [1, 1, 0]
        self.assertEqual(get_current_question(question_list, num), ('title', (None, ['string'])))
        question_list = [('first', (None, ['string'])), ('tasks', [('title', (None, ['string'])), ('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])})])]
        num = [1, 1, 1]
        self.assertEqual(get_current_question(question_list, num), ('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}))
        question_list = [('first', (None, ['string'])), ('tasks', [('title', (None, ['string'])), ('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])})])]
        num = [1, 1, 2]
        self.assertEqual(get_current_question(question_list, num), ('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])}))

    def test_get_question(self):
        question = ('question', 'question_data')
        question_list = [[[question, ()], (), ()], [()], ()]
        self.assertEqual(get_question(question_list), (question, [0, 0, 0]))
        question = ('question', 'question_data')
        question_list = [question, 'test']
        self.assertEqual(get_question(question_list), (question, [0]))

        question_list = ([('first', (None, ['string'])), ('tasks', [('title', (None, ['string'])), ('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])})])], {'title': None, 'tasks': [{'title': None, 'details': None, 'done': None}]})
        self.assertEqual(get_question(question_list), (('first', (None, ['string'])), [0, 0]))
        question_list = ([('tasks', [('title', (None, ['string'])), ('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])})])], {'title': None, 'tasks': [{'title': None, 'details': None, 'done': None}]})
        self.assertEqual(get_question(question_list), (('title', (None, ['string'])), [0, 0, 0]))
        question_list = ([('tasks', [('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), ('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])})])], {'title': None, 'tasks': [{'title': None, 'details': None, 'done': None}]})
        self.assertEqual(get_question(question_list), (('details', {'with_skip': ({"inline_keyboard": [[], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['string']), 'without_skip': (None, ['string'])}), [0, 0, 0]))
        question_list = ([('tasks', [('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])})])], {'title': None, 'tasks': [{'title': None, 'details': None, 'done': None}]})
        self.assertEqual(get_question(question_list), (('done', {'with_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}], [{"text": "Skip", "callback_data": "UniTurnipCancel"}]]}, ['boolean']), 'without_skip': ({"inline_keyboard": [[{"text": "Yes", "callback_data": "UniTurnipTrue"}, {"text": "No", "callback_data": "UniTurnipFalse"}]]}, ['boolean'])}), [0, 0, 0]))

if __name__ == '__main__':
    main()
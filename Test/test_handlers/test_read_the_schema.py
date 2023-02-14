from unittest import TestCase, main

from read_the_schema import SchemaRead, open_ref, get_question, required, pack_question, write_in_the_stencil


class TestSchemaRead(TestCase):
    def setUp(self):
        schema = {}
        self.Schema = SchemaRead(schema)

    def test_type_fork(self):
        pass

    def test_read_base_type(self):
        string_key = ''
        schema = ''
        object_data = None
        self.Schema.read_base_type(string_key, schema, object_data)




        

    def test_open_ref(self):
        ref = '#/test/test_test/'
        schema = {
            'test': {
                'test_test': {'toilet': '4', 'chair': '4'}
            }
        }
        result = {'toilet': '4', 'chair': '4'}
        self.assertEqual(open_ref(ref, schema), result)
        ref = '#/test/test_test/hehe'
        schema = {
            'start': 'Reade set Go!',
            'test': {
                'test_test': {'x': 'h', 'hehe': {'title': 'Title', 'description': '(facebook is ruled by a reptilian)'}}
            }
        }
        result = {'title': 'Title', 'description': '(facebook is ruled by a reptilian)'}
        self.assertEqual(open_ref(ref, schema), result)

    def test_get_question(self):
        save_data = {}
        get_data = {'title': 'Test', 'description': 'test'}
        result = {'question': 'Test\n(test)'}
        self.assertEqual(get_question(save_data, get_data), result)
        save_data = {'tie': 'long and red'}
        get_data = {'title': 'Test', 'description': 'test'}
        result = {'question': 'Test\n(test)', 'tie': 'long and red'}
        self.assertEqual(get_question(save_data, get_data), result)
        save_data = {'theory': 'masons exist'}
        get_data = {'title': 'Test'}
        result = {'question': 'Test', 'theory': 'masons exist'}
        self.assertEqual(get_question(save_data, get_data), result)
        save_data = {'theory': 'they are among us'}
        get_data = {'main_title': 'Personal space', 'main_description': 'Do you value personal space?'}
        result = {'question': 'Personal space\n(Do you value personal space?)', 'theory': 'they are among us'}
        self.assertEqual(get_question(save_data, get_data, main=True), result)
        save_data = {}
        get_data = {'main_title': 'Socks'}
        result = {'question': 'Socks'}
        self.assertEqual(get_question(save_data, get_data, main=True), result)

    def test_required(self):
        self.assertEqual(required({'required': ['test']}, 'test'), True)
        self.assertEqual(required({'required': []}, 'test'), False)
        self.assertEqual(required({'required': []}, 'test', required_=True), True)
        self.assertEqual(required({'required': ['test']}, 'test', required_=False), False)
        self.assertEqual(required(None, 'test'), False)
        self.assertEqual(required(None, 'test', required_=True), True)

    def test_pack_question(self):
        result = [({}, [])]
        self.assertEqual(pack_question({}, []), result)
        result = [({'test': 2342}, ['test', 'polymorphism'])]
        self.assertEqual(pack_question({'test': 2342}, ['test', 'polymorphism']), result)

    def test_write_in_the_stencil(self):
        schema = {}
        what_to_write__key = 'test'
        what_to_write__value = ''
        result = {'test': ''}
        self.assertEqual(write_in_the_stencil(schema, what_to_write__key, what_to_write__value), result)

        schema = [{}]
        what_to_write__key = 'key'
        what_to_write__value = None
        result = [{'key': None}]
        self.assertEqual(write_in_the_stencil(schema, what_to_write__key, what_to_write__value), result)

        schema = {}
        what_to_write__key = 'keyS'
        what_to_write__value = []
        result = {'keyS': []}
        self.assertEqual(write_in_the_stencil(schema, what_to_write__key, what_to_write__value), result)

        schema = [{}]
        what_to_write__key = 'key'
        what_to_write__value = []
        result = [{'key': []}]
        self.assertEqual(write_in_the_stencil(schema, what_to_write__key, what_to_write__value), result)

        schema = {}
        what_to_write__key = 'test_key'
        what_to_write__value = ['home', 'table', 'inertia', 'quicksand']
        result = {'test_key': ['home', 'table', 'inertia', 'quicksand']}
        self.assertEqual(write_in_the_stencil(schema, what_to_write__key, what_to_write__value), result)

        schema = [{}]
        what_to_write__key = 'test_key'
        what_to_write__value = ['home', 'table', 'inertia', 'quicksand']
        result = [{'test_key': ['home', 'table', 'inertia', 'quicksand']}]
        self.assertEqual(write_in_the_stencil(schema, what_to_write__key, what_to_write__value), result)


if __name__ == '__main__':
    main()

from UniTurnip_for_bots.handlers.tools import merge_dict


class SchemaRead:
    def __init__(self, schema):
        self.question_list = []
        self.schema = schema
        self.question_list = self.type_fork(schema)
        self.stencil = self.response_stencil(schema)

    def get(self):
        return self.question_list, self.stencil

    # ================================================================
    # ============================| fork |============================
    # ================================================================
    def type_fork(self, schema, key=None, object_data=None, required_=None):
        if 'type' in schema.keys():
            if schema['type'] == 'array':
                return self.read_array(key, schema, object_data)
            elif schema['type'] in ('string', 'integer', 'number', 'boolean'):
                return self.read_base_type(key, schema, object_data, required_=required_)
            elif schema['type'] == 'object':
                return self.read_object(schema, last_key=key, last_object_data=object_data)
            else:
                raise TypeError(f'schema["type"] = {schema["type"]}')
        elif '$ref' in schema.keys():
            schema = open_ref(schema['$ref'], self.schema)
            return self.type_fork(schema, key=key, object_data=object_data, required_=required_)
        else:
            raise KeyError(schema.keys(), schema)

    # ================================================================
    # ====================| Read differance type |====================
    # ================================================================
    def read_object(self, object, last_key=None, last_object_data=None):
        object_data = self.create_object_data(object, last_key=last_key, last_object_data=last_object_data)
        if 'properties' in object.keys():
            return self.unpack_object(object['properties'], object_data)
        elif 'items' in object.keys():
            return self.unpack_object(object['items'], object_data)
        else:
            raise KeyError(f'"properties" and "items" not in object.keys(). object = {object}')

    # ----------------------------------------------------------------
    def read_array(self, array_key, array, last_object_data):
        current_object_data = self.create_object_data(array, last_key=array_key, last_object_data=last_object_data)
        if type(array['items']) == dict:
            return self.type_fork(array['items'], key=array_key, object_data=current_object_data)
        elif type(array['items']) == list:
            question_array = []
            for value in array['items']:
                question_array += [self.type_fork(value, key='', object_data=current_object_data, required_=True)]
            if 'additionalItems' in array.keys():
                question_array += [self.type_fork(array['additionalItems'], key='',
                                                  object_data=current_object_data, required_=False)]
            return question_array

    # ----------------------------------------------------------------
    def read_base_type(self, string_key, schema, object_data, required_=None):
        question_data = self.create_question(schema, object_data)
        question_data['required'] = required(object_data, string_key, required_=required_)
        # question_data = required_keyboard(question_data)
        return question_data

    # ----------------------------------------------------------------
    def read_dependencies(self, dependencies):
        dependencies_data = []
        for key_q, value in dependencies.items():
            for name_q, data in value.items():
                dependencies_data += self.create_question_options(data, key_q)
        return dependencies_data

    # ================================================================
    # =========================| Unpacking |==========================
    # ================================================================
    def unpack_object(self, items, object_data):
        questions_list = []
        for key, value in items.items():
            question_data = self.type_fork(value, key=key, object_data=object_data)
            questions_list += pack_question(key, question_data)
        return questions_list

    # ================================================================
    # ========================| Create data |=========================
    # ================================================================
    def create_question(self, schema, object_data):
        if 'title' in schema.keys():
            question = get_question(schema, schema)
        elif object_data is None:
            return {}
        elif 'main_title' in object_data.keys():
            question = get_question(schema, object_data, main=True)
        elif 'main_title' in object_data['last_object_data'].keys():
            question = get_question(schema, object_data["last_object_data"], main=True)
        else:
            raise KeyError('Title not found')
        return merge_dict(question, object_data)

    # ----------------------------------------------------------------
    def create_object_data(self, object, last_key=None, last_object_data=None):
        object_data = {
            'main_type': 'object',
            'required': [] if 'required' not in object.keys() else object['required']
        }
        if last_key:
            object_data['last_key'] = last_key
            object_data['last_object_data'] = last_object_data
        if 'dependencies' in object.keys():
            object_data['dependencies'] = self.read_dependencies(object['dependencies'])
        if 'required' in object.keys():
            object_data['required'] = object['required']
        if 'title' in object.keys():
            object_data['main_title'] = object['title']
        if 'description' in object.keys():
            object_data['main_description'] = object['description']
        return object_data

    # ----------------------------------------------------------------
    def create_question_options(self, object_, main_q_name):
        question_options = []
        if type(object_) == list:
            for value in object_:
                if type(value) == dict:
                    if 'properties' in value.keys():
                        question_options += self.create_option(value['properties'], main_q_name)
            return question_options
        else:
            raise TypeError(type(object_))

    # ----------------------------------------------------------------
    def create_option(self, properties, main_question_name):
        answer = properties[main_question_name]['enum']
        additional_q = []
        for key, value in properties.items():
            if key == main_question_name:
                continue
            else:
                value['title'] = key
                additional_q += [(answer, self.type_fork(value))]
        return additional_q

    # ======================================================================================
    # ================================| create the stencil |================================
    # ======================================================================================
    def response_stencil(self, schema, ref=None):
        if ref:
            return self.unpacking_a_dictionary_with_different_questions(schema, ref['properties'].items())
        if type(schema) == dict:
            if 'type' in schema:
                if 'properties' in schema.keys():
                    properties = schema['properties'].items()
                elif 'items' in schema.keys():
                    if type(schema['items']) == dict:
                        if '$ref' in schema['items'].keys():
                            ref = schema['items']['$ref']
                            return self.response_stencil(schema, ref=open_ref(ref, self.schema))
                        elif schema['items']['type'] == 'object':
                            properties = schema['items']['properties'].items()
                        elif schema['items']['type'] in ('string', ''):
                            return []
                        elif schema['items']['type'] == 'array':
                            return [[]]
                        else:
                            raise (schema['items']['type'])
                    elif type(schema['items']) == list:
                        return []
                    else:
                        raise TypeError(type(schema['items']), schema['items'])
                else:
                    return None
                return self.unpacking_a_dictionary_with_different_questions(schema, properties)

    # --------------------------------------------------------------------------------------
    def unpacking_a_dictionary_with_different_questions(self, schema, dictionary):
        if schema['type'] == 'array':
            key_list = [{}]
        elif schema['type'] == 'object':
            key_list = {}
        else:
            raise TypeError(schema['type'])
        for key, value in dictionary:
            if type(value) == dict and 'type' in value:
                write_in_the_stencil(key_list, key, self.response_stencil(value))
            else:
                write_in_the_stencil(key_list, key, None)
        return key_list
    # ======================================================================================


# ================================================
# ===================| Tools |====================
# ================================================
def open_ref(ref, schema):
    if type(ref) == str:
        ref = ref.split('/')[1:]
    if len(ref) != 0 and ref[0]:
        res = schema[ref[0]]
        return open_ref(ref[1:], res)
    else:
        return schema


# ------------------------------------------------
def get_question(save_data, get_data, main=False):
    if main:
        save_data['question'] = get_data['main_title']
        description_key = 'main_description'
    else:
        save_data['question'] = get_data['title']
        description_key = 'description'
    if description_key in get_data.keys():
        save_data['question'] += f'\n({get_data[description_key]})'
    return save_data


# ------------------------------------------------
def required(object_data, key, required_=None):
    if required_ is None and object_data:
        if key in object_data['required']:
            return True
        else:
            return False
    elif required_ is not None:
        return required_
    else:
        return False


# ------------------------------------------------
def pack_question(question_name, question_data):
    return [(question_name, question_data)]


# ------------------------------------------------
def write_in_the_stencil(schema, what_to_write__key, what_to_write__value):
    if type(schema) == list:
        schema[0][what_to_write__key] = what_to_write__value
    elif type(schema) == dict:
        schema[what_to_write__key] = what_to_write__value
    else:
        raise TypeError(type(schema))
    return schema
# ================================================


if __name__ == '__main__':
    from UniTurnip_for_bots.handlers.constants import dependencies

    def print_with_indent(indent, string=None, line_break=False):
        print('    ' * indent, end='')
        if string:
            print(string)
        if line_break:
            print()

    def print_frame(indent, len_add_q_name, new_string=False):
        if new_string:
            print()
        print_with_indent(indent)
        print('=' * (len_add_q_name + 4))

    def print_result(result, start=False, indent=0):
        if start:
            print(f'result = {result}\n')
        for res in result:
            if type(res) == tuple:
                if type(res[1]) == dict:
                    print_with_indent(indent, string=res[0])
                    print_with_indent(indent, string=res[1])
                elif type(res[1]) == list:
                    print_frame(indent, len(res[0]), new_string=True)
                    print_with_indent(indent, string=f'| {res[0]} | ({indent})')
                    print_frame(indent, len(res[0]))
                    print_result(res[1], indent=indent+1)
            else:
                print_with_indent(indent, string=res)

    schema = dependencies
    Schema = SchemaRead(schema)

    print_result(Schema.get(), start=True)


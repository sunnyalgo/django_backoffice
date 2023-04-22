def code_to_name(code_str):
    return code_str.replace('_', ' ')


def create_choices_tuple(choices_list):
    return tuple((item_code, code_to_name(item_code))
                 for item_code in choices_list)

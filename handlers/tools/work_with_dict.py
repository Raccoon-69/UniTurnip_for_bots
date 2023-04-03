def merge_dict(dict1, dict2):
    if dict1 and dict2:
        dict1.update(dict2)
        return dict1
    elif dict1 is None and dict2:
        return dict2
    elif dict2 is None and dict1:
        return dict1
    else:
        return None
collection = get_list()
key = 0
try:
    return handle_value(collection[key])
except KeyError:
    return key_not_found(key)
key = 0
collection = get_list()
try:
    return handle_value(collection[key])
except KeyError:
    return key_not_found(key)
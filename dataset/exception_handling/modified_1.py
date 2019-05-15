key = 0
collection = get_list()
try:
    value = collection[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)
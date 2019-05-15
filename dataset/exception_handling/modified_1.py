collection = get_list()
key = 0
try:
    value = collection[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)
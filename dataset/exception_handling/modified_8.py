collection = []
try:
    value = collection['key']
except KeyError:
    return key_not_found(key)
else:
    return calculate(value)
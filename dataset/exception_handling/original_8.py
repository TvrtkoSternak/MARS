collection = []
try:
    return calculate(collection['key'])
except KeyError:
    return key_not_found('key')
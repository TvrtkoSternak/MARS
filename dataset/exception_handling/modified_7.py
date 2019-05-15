try:
    obj = json.load(json_object)
except json.JSONDecodeError:
    return bad_json(json_object)
else:
    return do_something_with_json(obj)
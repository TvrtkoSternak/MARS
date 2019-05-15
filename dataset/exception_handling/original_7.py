try:
    return do_something_with_json(json.load(json_object))
except json.JSONDecodeError:
    return bad_json(json_object)
no_error = None
try:
    try_this(whatever)
    no_error = True
except SomeException as the_exception:
    handle(the_exception)
if no_error:
    return something
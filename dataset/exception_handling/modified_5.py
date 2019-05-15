try:
    try_this(whatever)
except SomeException as the_exception:
    handle(the_exception)
else:
    return something
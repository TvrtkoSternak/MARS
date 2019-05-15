x = 0
try:
    y = 1/x
except ZeroDivisionError:
    return None
else:
    return squared(y)
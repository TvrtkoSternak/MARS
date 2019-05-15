y = 0
try:
    x = 1/y
except ZeroDivisionError:
    return None
else:
    return squared(x)
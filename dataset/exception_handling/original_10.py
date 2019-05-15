y = float("inf")
try:
    return squared(1/y)
except ZeroDivisionError:
    return None
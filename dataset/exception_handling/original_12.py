numbers = [1, 2, 3, 4]
i = 5
try:
    return do_something(numbers[i])
except IndexError:
    return len(numbers)
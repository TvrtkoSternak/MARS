numbers = [1, 2, 3, 4]
i = 5
try:
    x = numbers[i]
except IndexError:
    return len(numbers)
else:
    return do_something(x)
try:
    with open("a.txt") as f:
        print(f.readlines())
except EnvironmentError:
    # Handle error
    print('failed to read from file')

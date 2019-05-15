with open("read/this/file", "r") as file:
    for line in file.readlines():
        if line.startswith("start"):
            print(line)
file = open("read/this/file", "r")

for line in file.readlines():
    if line.startswith("start"):
        print(line)

file.close()
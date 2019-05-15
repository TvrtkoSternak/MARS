with open("path/to/reading", "r") as file_to_read, open("path/to/write", "w") as file_to_write:
    for line in file_to_read.readlines():
        file_to_write.write(line)
file_to_read = open("path/to/reading", "r")
file_to_write = open("path/to/write", "w")

for line in file_to_read.readlines():
    file_to_write.write(line)

file_to_read.close()
file_to_write.close()
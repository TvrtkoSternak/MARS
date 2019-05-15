file_one = open("filepath", "w")
file_two = open("filepath2", "rb")

for line in file_two.read():
    file_two.write(from_bin_to_str(line))
    print("recalculated line")

file_one.close()
file_two.close()
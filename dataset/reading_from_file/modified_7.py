with open("filepath", "w") as file_one, open("filepath2", "rb") as file_two:
    for line in file_two.read():
        file_two.write(from_bin_to_str(line))
        print("recalculated line")
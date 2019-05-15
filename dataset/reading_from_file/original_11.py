file_for_one_data = open("file/one/data", "w")
file_for_other_data = open("file/other/data", "w")

for number in numbers:
    if some_number_condition(number):
        file_for_one_data.write(number)
    else:
        file_for_other_data.write(number)

file_for_one_data.close()
file_for_other_data.close()
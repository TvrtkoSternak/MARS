with open("file/one/data", "w") as file_for_one_data, open("file/other/data", "w") as file_for_other_data:
    for number in numbers:
        if some_number_condition(number):
            file_for_one_data.write(number)
        else:
            file_for_other_data.write(number)
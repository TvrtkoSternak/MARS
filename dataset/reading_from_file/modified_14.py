with open("bytes/files/file", "rb") as file_to_read_two_byte_data:
    first_byte = file_to_read_two_byte_data.read(1)
    second_byte = file_to_read_two_byte_data.read(1)
    calculate_bytes(first_byte, second_byte)
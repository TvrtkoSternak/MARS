file_to_read_two_byte_data = open("bytes/files/file", "rb")

first_byte = file_to_read_two_byte_data.read(1)
second_byte = file_to_read_two_byte_data.read(1)
calculate_bytes(first_byte, second_byte)

file_to_read_two_byte_data.close()

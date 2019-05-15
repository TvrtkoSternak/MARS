some_filename = open("file_binary", "rb")

for byte in some_filename.read():
    binary_calculations_to_be_done(byte)

some_filename.close()
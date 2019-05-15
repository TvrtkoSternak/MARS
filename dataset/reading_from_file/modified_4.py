with open("file_binary", "rb") as some_filename:
    for byte in some_filename.read():
        binary_calculations_to_be_done(byte)
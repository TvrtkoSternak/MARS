try:
    file = open('input-file', 'open mode')
except EOFError as ex:
    print("Caught the EOF error.")
except IOError as e:
    print("Caught the I/O error.")

try:
    file = open('input-file', 'open mode')
except (IOError, EOFError) as e:
    if type(e) is IOError:
        print("Caught the I/O error.")
    elif type(e) is EOFError:
        print("Caught the EOF error.")

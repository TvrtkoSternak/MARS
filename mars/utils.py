import datetime


class Diagnostics:
    __instance = None
    count = 0

    @staticmethod
    def get_instance():
        if Diagnostics.__instance is None:
            Diagnostics()
        return Diagnostics.__instance

    def __init__(self):
        if Diagnostics.__instance:
            raise Exception("This class is a singleton!")
        else:
            Diagnostics.__instance = self
            Diagnostics.count = 1
            with open("../resources/diagnostics.txt", "w+") as log:
                print("Diagnostics ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), file=log)

    @staticmethod
    def log(first_pattern, second_pattern, created_pattern):
        with open("../resources/diagnostics.txt", "a") as log:
            print("----------------------------------------", file=log)

            print("Pattern #", Diagnostics.count, file=log)
            print("Original #1 {", file=log)
            print(first_pattern.original.to_source_code(0), end='', file=log)
            print("}", file=log)
            print(file=log)

            print("Original #2 {", file=log)
            print(second_pattern.original.to_source_code(0), end='', file=log)
            print("}", file=log)
            print(file=log)

            print("Original Created {", file=log)
            print(created_pattern.original.to_source_code(0), end='', file=log)
            print("}", file=log)
            print(file=log)

            print("Modified #1 {", file=log)
            print(first_pattern.modified.to_source_code(0), end='', file=log)
            print("}", file=log)
            print(file=log)

            print("Modified #2 {", file=log)
            print(second_pattern.modified.to_source_code(0), end='', file=log)
            print("}", file=log)
            print(file=log)

            print("Modified Created {", file=log)
            print(created_pattern.modified.to_source_code(0), end='', file=log)
            print("}", file=log)
            print(file=log)

            Diagnostics.count += 1

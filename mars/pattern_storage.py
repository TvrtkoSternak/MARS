import pickle

filename = "../resources/patterns.p"


class StorageContext:

    @staticmethod
    def save(pattern):
        with open(filename, 'ab') as storage:
            pickle.dump(pattern, storage)

    @staticmethod
    def load():
        patterns = []
        with open(filename, 'rb') as storage:
            while 1:
                try:
                    patterns.append(pickle.load(storage))
                except EOFError:
                    break

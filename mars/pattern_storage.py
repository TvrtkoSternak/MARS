import pickle

filename = "patterns.p"


class StorageContext:

    @staticmethod
    def save(pattern):
        with open(filename) as storage:
            pickle.dump(pattern, storage)

    @staticmethod
    def load():
        patterns = []
        with open(filename) as storage:
            while 1:
                try:
                    patterns.append(pickle.load(storage))
                except EOFError:
                    break

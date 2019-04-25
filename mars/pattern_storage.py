import pickle

filename = "../resources/patterns.p"


class StorageContext:

    def __init__(self, file):
        self.filename = file

    def save(self, pattern):
        with open(self.filename, 'ab') as storage:
            pickle.dump(pattern, storage)

    def load(self):
        patterns = []
        with open(self.filename, 'rb') as storage:
            while 1:
                try:
                    patterns.append(pickle.load(storage))
                except EOFError:
                    break

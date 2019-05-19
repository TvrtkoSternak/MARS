import pickle


class StorageContext:

    def __init__(self, file = "../resources/patterns.p"):
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
        return patterns

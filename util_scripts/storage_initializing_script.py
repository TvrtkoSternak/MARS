import os

from mars.astutils import AstWrapper
from mars.pattern_creation import PatternCreator, TreeDifferencer
from mars.pattern_storage import StorageContext

pattern_creator = PatternCreator(TreeDifferencer(0.3), AstWrapper())
storage_context = StorageContext()
storage_context.delete()

for directory, children, files in os.walk("../dataset"):
    if directory.split('/')[-1] not in 'dataset':
        print(directory)

        if "testing_small" in str(directory):
            for i in range(1, int(len(os.listdir(directory))/2)+1):
                try:
                    file_org = directory + "/original_" + i.__str__() + ".py"
                    file_mod = directory + "/modified_" + i.__str__() + ".py"
                    pattern = pattern_creator.create_pattern(file_org, file_mod)
                    storage_context.save(pattern)
                except Exception as e:
                    print(i)


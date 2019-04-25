from mars.pattern_creation import PatternCreator, EditScriptGenerator, TreeDifferencer
from mars.pattern_parsing import CounterPatternParser

parser = CounterPatternParser()
script_generator = EditScriptGenerator(TreeDifferencer(2, 0, 0), 0)
pattern_creator = PatternCreator(None, parser, script_generator)

for i in range(1, 5):
    file_org = "../resources/pattern_"+i.__str__()+"_org.pat"
    file_mod = "../resources/pattern_"+i.__str__()+"_mod.pat"
    pattern = pattern_creator.create_pattern(file_org, file_mod)
    pattern_creator.save_pattern(pattern)

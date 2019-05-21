from mars.astutils import AstWrapper
from mars.pattern_creation import PatternCreator, TreeDifferencer

pattern_creator = PatternCreator(TreeDifferencer(0.3), AstWrapper())

pattern = pattern_creator.create_pattern("../dataset/some_shit/original_3.py", "../dataset/some_shit/modified_3.py")
print(pattern.node_pairs)
import ast

from mars.astutils import AstWrapper
from mars.pattern_creation import TreeDifferencer
from mars.pattern_creation import EditScriptGenerator

with open("../dataset/variable_check/original_4.py") as original, open("../dataset/variable_check/original_5.py") as modified:
    original_code = ast.parse(original.read())
    modified_code = ast.parse(modified.read())

wrapper = AstWrapper()

org = wrapper.visit(original_code)
mod = wrapper.visit(modified_code)

tree_diff = TreeDifferencer(0.1)
# tree_diff.connect_nodes(org, mod)

generator = EditScriptGenerator(tree_diff, 0.3)
edit_script = generator.generate(org, mod)

org = org.walk()

edit_script.execute(org)

org[0].reconstruct(org).unparse(0)


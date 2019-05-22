import ast

from mars.astutils import AstWrapper
from mars.pattern_creation import TreeDifferencer
from mars.pattern_creation import EditScriptGenerator

with open("../dataset/true/original_17.py") as original, open("../dataset/true/modified_17.py") as modified:
    original_code = ast.parse(original.read())
    modified_code = ast.parse(modified.read())

wrapper = AstWrapper()

org = wrapper.visit(original_code)
mod = wrapper.visit(modified_code)

# tree_diff = TreeDifferencer(0.1)
# # tree_diff.connect_nodes(org, mod)
#
# generator = EditScriptGenerator(tree_diff, 0.3)
# edit_script = generator.generate(org, mod)

org = org.walk()
mod =  mod.walk()

# edit_script.execute(org)

org.pop(0).reconstruct(org).unparse(0)
mod.pop(0).reconstruct(mod).unparse(0)


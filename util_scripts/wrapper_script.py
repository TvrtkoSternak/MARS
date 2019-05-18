import ast

from mars.astutils import AstWrapper
from mars.pattern_creation import TreeDifferencer
from mars.pattern_creation import EditScriptGenerator

with open("../dataset/variable_check/original_6.py") as original, open("../dataset/variable_check/modified_6.py") as modified:
    original_code = ast.parse(original.read())
    modified_code = ast.parse(modified.read())

wrapper = AstWrapper()

org = wrapper.visit(original_code)
mod = wrapper.visit(modified_code)

tree_diff = TreeDifferencer(0.1)
# tree_diff.connect_nodes(org, mod)

generator = EditScriptGenerator(tree_diff, 0.3)
generator.generate(org, mod)

# wrapper = AstWrapper()
# body = wrapper.visit(original_code)
#
# body.print_me()
# body.unparse(0)
#
# tree = body.walk(postorder=True)
#
# print(tree)
# re = tree.pop(0).reconstruct(tree)
#
# print("----------------")
# re.unparse(0)

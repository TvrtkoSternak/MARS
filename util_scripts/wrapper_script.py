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
for index, node in enumerate(org):
    print(index, node)
offset = 0
edit_script.execute(org)
# for change in edit_script:
#     for index, node in enumerate(org):
#         print(index, node)
#
#     print(change)
#     try:
#         change.change.unparse(0)
#         print()
#     except:
#         pass
#     org, offset_add = change.make_change(org, offset)
#     offset += offset_add
    # org = org[0].reconstruct(org)
    # org.unparse(0)
    # org = org.walk()
    # print()

org[0].reconstruct(org).unparse(0)

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

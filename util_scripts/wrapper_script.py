import ast

from mars.astutils import AstWrapper
from mars.astwrapper import Body

with open("../dataset/variable_check/original_1.py") as original:
    original_code = ast.parse(original.read())

wrapper = AstWrapper()
body = wrapper.visit(original_code)

body.print_me()
body.unparse(0)

tree = body.walk(postorder=True)

print(tree)
re = tree.pop(0).reconstruct(tree)

print("----------------")
re.unparse(0)

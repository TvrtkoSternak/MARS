import ast

from mars.astutils import AstWrapper

with open("../dataset/variable_check/original_1.py") as original:
    original_code = ast.parse(original.read())

wrapper = AstWrapper()
body = wrapper.visit(original_code)

body.print_me()
body.unparse(0)

print(body.walk())
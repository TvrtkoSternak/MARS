import ast

from mars.astutils import AstWrapper

with open("../dataset/variable_check/original_1.py") as original:
    original_code = ast.parse(original.read())

wrapper = AstWrapper()
wrapper.visit(original_code).print_me()

body = wrapper.body

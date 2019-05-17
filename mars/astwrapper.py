class Variable:
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("Variable {", self.value, "}")

    def unparse(self, num_tabs):
        print(self.value, end = '')


class Constant:
    def __init__(self, value, type_of):
        self.value = value
        self.type_of = type_of

    def print_me(self):
        print("Constant {", self.type_of, " ", self.value, " }")

    def unparse(self, num_tabs):
        print(self.value, end='')


class Assign:
    def __init__(self, variable, operation, value):
        self.variable = variable
        self.operation = operation
        self.value = value

    def print_me(self):
        print("Assign: {")
        self.variable.print_me()
        print(self.operation)
        self.value.print_me()
        print("}")

    def unparse(self, num_tabs):
        self.variable.unparse(num_tabs)
        print(" = ", end='')
        self.value.unparse(num_tabs)


class Function:
    def __init__(self, args, value):
        self.args = args
        self.value = value

    def print_me(self):
        print(self.value, "{")
        for arg in self.args:
            arg.print_me()
        print("}")

    def unparse(self, num_tabs):
        print("{0}(".format(self.value), end='')
        for arg in self.args:
            arg.unparse(num_tabs)
        print(")", end='')


class Condition:
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("Condition {")
        self.value.print_me()
        print("}")

    def unparse(self, num_tabs):
        self.value.unparse(num_tabs)


class ElIf:
    def __init__(self, condition, body, next_if):
        self.condition = condition
        self.body = body
        self.next_if = next_if

    def print_me(self):
        print("If {")
        self.condition.print_me()
        self.body.print_me()
        self.next_if.print_me()
        print("}")

    def unparse(self, num_tabs):
        print("\t"*num_tabs, "elif ", end='', sep='')
        self.condition.unparse(num_tabs)
        print(":")
        self.body.unparse(num_tabs + 1)
        self.next_if.unparse(num_tabs)

class Else:
    def __init__(self, body):
        self.body = body

    def print_me(self):
        print("Else {")
        self.body.print_me()
        print("}")

    def unparse(self, num_tabs):
        print("\t"*num_tabs, "else:", sep='')
        self.body.unparse(num_tabs + 1)

class If:
    def __init__(self, condition, body, next_if):
        self.condition = condition
        self.body = body
        self.next_if = next_if

    def print_me(self):
        print("If {")
        self.condition.print_me()
        self.body.print_me()
        self.next_if.print_me()
        print("}")

    def unparse(self, num_tabs):
        print("if ", end='')
        self.condition.unparse(num_tabs)
        print(":")
        self.body.unparse(num_tabs + 1)
        self.next_if.unparse(num_tabs)


class Body:
    def __init__(self, children):
        self.children = children

    def print_me(self):
        print("Body {")
        for child in self.children:
            child.print_me()
        print("}")

    def unparse(self, num_tabs):
        for child in self.children:
            print("\t"*num_tabs, end='')
            child.unparse(num_tabs)
            if not hasattr(child, 'body'):
                print()


class BoolOperation:
    def __init__(self, operation, first, second):
        self.operation = operation
        self.first = first
        self.second = second

    def print_me(self):
        self.first.print_me()
        print(self.operation)
        self.second.print_me()

    def unparse(self, num_tabs):
        self.first.unparse(num_tabs)
        print("", self.operation, "", end='')
        self.second.unparse(num_tabs)


class UnaryOperation:
    def __init__(self, operation, first):
        self.operation = operation
        self.first = first

    def print_me(self):
        print(self.operation, " {")
        self.first.print_me()
        print("}")

    def unparse(self, num_tabs):
        print(self.operation, "", end='')
        self.first.unparse(num_tabs)


class Compare:
    def __init__(self, operation, first, second):
        self.operation = operation
        self.first = first
        self.second = second

    def print_me(self):
        print("{")
        self.first.print_me()
        print(self.operation)
        self.second.print_me()
        print("}")

    def unparse(self, num_tabs):
        self.first.unparse(num_tabs)
        print("", self.operation, "", end='')
        self.second.unparse(num_tabs)


class EmptyNode:
    def print_me(self):
        pass

    def unparse(self, num_tabs):
        pass


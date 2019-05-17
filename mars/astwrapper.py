class Variable:
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("Variable {", self.value, "}")


class Constant:
    def __init__(self, value, type_of):
        self.value = value
        self.type_of = type_of

    def print_me(self):
        print("Constant {", self.type_of, " ", self.value, " }")


class Assign:
    def __init__(self, variable, operation, value):
        self.variable = variable
        self.operation = operation
        self.value = value

    def print_me(self):
        print("Assign: {")
        self.variable.print_me()
        self.operation.print_me()
        self.value.print_me()
        print("}")


class Function:
    def __init__(self, args, value):
        self.args = args
        self.value = value

    def print_me(self):
        print(self.value, "{")
        for arg in self.args:
            arg.print_me()
        print("}")


class Condition:
    def __init__(self, children):
        self.children = children

    def print_me(self):
        print("Condition {")
        for child in self.children:
            child.print_me()
        print("}")


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


class Body:
    def __init__(self, children):
        self.children = children

    def print_me(self):
        print("Body {")
        for child in self.children:
            child.print_me()
        print("}")

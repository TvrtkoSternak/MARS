class Variable:
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("Variable {", self.value, "}")

    def unparse(self, num_tabs):
        print(self.value, end = '')

    def walk(self):
        return self


class Constant:
    def __init__(self, value, type_of):
        self.value = value
        self.type_of = type_of

    def print_me(self):
        print("Constant {", self.type_of, " ", self.value, " }")

    def unparse(self, num_tabs):
        print(self.value, end='')

    def walk(self):
        return self


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
        print(self.operation, end='')
        self.value.unparse(num_tabs)

    def walk(self):
        tree = list()
        tree.append(self)
        tree.append(Startnode())
        tree.append(self.variable.walk())
        tree.append(self.value.walk())
        tree.append(Endnode())
        return tree


class FunctionName:
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("FunctionName {", self.value, "}")

    def unparse(self, num_tabs):
        print("{0}(".format(self.value), end='')

    def walk(self):
        return self

class Function:
    def __init__(self, args, value):
        self.args = args
        self.value = value

    def print_me(self):
        print("Function {")
        self.value.print_me()
        for arg in self.args:
            arg.print_me()
        print("}")

    def unparse(self, num_tabs):
        self.value.unparse(num_tabs)
        for arg in self.args:
            arg.unparse(num_tabs)
        print(")", end='')

    def walk(self):
        tree = list()
        tree.append(self)
        tree.append(Startnode())
        tree.append(self.value.walk())
        for arg in self.args:
            tree.append(arg.walk())
        tree.append(Endnode())
        return tree


class Condition:
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("Condition {")
        self.value.print_me()
        print("}")

    def unparse(self, num_tabs):
        self.value.unparse(num_tabs)

    def walk(self):
        tree = list()
        tree.append(self)
        tree.append(self.value.walk())
        return tree


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

    def walk(self):
        tree = list()
        tree.append(self)
        tree.append(self.condition.walk())
        tree.append(self.body.walk())
        tree.append(self.next_if.walk())
        return tree


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

    def walk(self):
        tree = list()
        tree.append(self)
        tree.append(self.body.walk())
        return tree


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

    def walk(self):
        tree = list()
        tree.append(self)
        tree.append(self.body.walk())
        tree.append(self.next_if.walk())
        return tree


class Body:
    def __init__(self, children):
        self.children = children
        self.children.insert(0, Startnode())
        self.children.append(Endnode())

    def print_me(self):
        print("Body {")
        for child in self.children:
            child.print_me()
        print("}")

    def unparse(self, num_tabs):
        for child in self.children:
            if not isinstance(child, (Startnode, Endnode)):
                print("\t"*num_tabs, end='')
            child.unparse(num_tabs)
            if not hasattr(child, 'body') and not isinstance(child, (Startnode, Endnode)):
                print()

    def walk(self):
        tree = list()
        tree.append(self)
        for child in self.children:
            tree.append(child.walk())
        return tree


class BoolOperation:
    def __init__(self, operation, first, second):
        self.operation = operation
        self.first = first
        self.second = second

    def print_me(self):
        self.first.print_me()
        self.operation.print_me()
        self.second.print_me()

    def unparse(self, num_tabs):
        self.first.unparse(num_tabs)
        self.operation.unparse(num_tabs)
        self.second.unparse(num_tabs)

    def walk(self):
        tree = list()
        tree.append(self)
        tree.append(self.first.walk())
        tree.append(self.operation.walk())
        tree.append(self.second.walk())
        return tree


class UnaryOperation:
    def __init__(self, operation, first):
        self.operation = operation
        self.first = first

    def print_me(self):
        self.operation.print_me()
        self.first.print_me()
        print("}")

    def unparse(self, num_tabs):
        self.operation.unparse(num_tabs)
        self.first.unparse(num_tabs)

    def walk(self):
        tree = list()
        tree.append(self)
        tree.append(self.operation.walk())
        tree.append(self.first.walk())
        return tree


class Compare:
    def __init__(self, operation, first, second):
        self.operation = operation
        self.first = first
        self.second = second

    def print_me(self):
        print("{")
        self.first.print_me()
        self.operation.print_me()
        self.second.print_me()
        print("}")

    def unparse(self, num_tabs):
        self.first.unparse(num_tabs)
        self.operation.unparse(num_tabs)
        self.second.unparse(num_tabs)

    def walk(self):
        tree = list()
        tree.append(self)
        tree.append(self.first.walk())
        tree.append(self.opeeration.walk())
        tree.append(self.second.walk())
        return tree


class EmptyNode:
    def print_me(self):
        pass

    def unparse(self, num_tabs):
        pass

    def walk(self):
        return self


class Startnode:
    def print_me(self):
        print("Start Node")

    def unparse(self, num_tabs):
        pass

    def walk(self):
        return self


class Endnode:
    def print_me(self):
        print("End Node")

    def unparse(self, num_tabs):
        pass

    def walk(self):
        return self

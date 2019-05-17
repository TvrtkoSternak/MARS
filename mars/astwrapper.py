class Variable:
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("Variable {", self.value, "}")

    def unparse(self, num_tabs):
        print(self.value, end = '')

    def walk(self):
        return [self]

    def reconstruct(self, tree):
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
        return [self]

    def reconstruct(self, tree):
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
        print('', self.operation, '', end='')
        self.value.unparse(num_tabs)

    def walk(self):
        tree = list()
        tree.append(self)
        tree.extend(self.variable.walk())
        tree.extend(self.value.walk())
        return tree

    def reconstruct(self, tree):
        self.variable = tree.pop(0).reconstruct(tree)
        self.value = tree.pop(0).reconstruct(tree)
        return self


class FunctionName:
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("FunctionName {", self.value, "}")

    def unparse(self, num_tabs):
        print("{0}(".format(self.value), end='')

    def walk(self):
        return [self]

    def reconstruct(self, tree):
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
        tree.extend(self.value.walk())
        for arg in self.args:
            tree.extend(arg.walk())
        tree.append(Endnode())
        return tree

    def reconstruct(self, tree):
        self.args.clear()
        tree.pop(0)
        self.value = tree.pop(0).reconstruct(tree)
        child = tree.pop(0)
        while not isinstance(child, Endnode):
            self.args.append(child.reconstruct(tree))
            child = tree.pop(0)
        return self


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
        tree.extend(self.value.walk())
        return tree

    def reconstruct(self, tree):
        self.value = tree.pop(0).reconstruct(tree)
        return self


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
        tree.extend(self.condition.walk())
        tree.extend(self.body.walk())
        tree.extend(self.next_if.walk())
        return tree

    def reconstruct(self, tree):
        self.condition = tree.pop(0).reconstruct(tree)
        self.body = tree.pop(0).reconstruct(tree)
        self.next_if = tree.pop(0).reconstruct(tree)
        return self


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
        tree.extend(self.body.walk())
        return tree

    def reconstruct(self, tree):
        self.body = tree.pop(0).reconstruct(tree)
        return self


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
        tree.extend(self.condition.walk())
        tree.extend(self.body.walk())
        tree.extend(self.next_if.walk())
        return tree

    def reconstruct(self, tree):
        self.condition = tree.pop(0).reconstruct(tree)
        self.body = tree.pop(0).reconstruct(tree)
        self.next_if = tree.pop(0).reconstruct(tree)
        return self


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

    def walk(self):
        tree = list()
        tree.append(self)
        tree.append(Startnode())
        for child in self.children:
            tree.extend(child.walk())
        tree.append(Endnode())
        return tree

    def reconstruct(self, tree):
        self.children.clear()
        tree.pop(0)
        child = tree.pop(0)
        while not isinstance(child, Endnode):
            self.children.append(child.reconstruct(tree))
            child = tree.pop(0)
        return self


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
        tree.extend(self.first.walk())
        tree.extend(self.operation.walk())
        tree.extend(self.second.walk())
        return tree

    def reconstruct(self, tree):
        self.first = tree.pop(0).reconstruct(tree)
        self.operation = tree.pop(0).reconstruct(tree)
        self.second = tree.pop(0).reconstruct(tree)
        return self


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
        tree.extend(self.operation.walk())
        tree.extend(self.first.walk())
        return tree

    def reconstruct(self, tree):
        self.operation = tree.pop(0).reconstruct(tree)
        self.first = tree.pop(0).reconstruct(tree)
        return self


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
        tree.extend(self.first.walk())
        tree.extend(self.operation.walk())
        tree.extend(self.second.walk())
        return tree

    def reconstruct(self, tree):
        self.first = tree.pop(0).reconstruct(tree)
        self.operation = tree.pop(0).reconstruct(tree)
        self.second = tree.pop(0).reconstruct(tree)
        return self


class EmptyNode:
    def print_me(self):
        pass

    def unparse(self, num_tabs):
        pass

    def walk(self):
        return [self]

    def reconstruct(self, tree):
        return self


class Startnode:
    def print_me(self):
        print("Start Node")

    def unparse(self, num_tabs):
        pass

    def walk(self):
        return [self]

    def reconstruct(self, tree):
        return self


class Endnode:
    def print_me(self):
        print("End Node")

    def unparse(self, num_tabs):
        pass

    def walk(self):
        return [self]

    def reconstruct(self, tree):
        return self

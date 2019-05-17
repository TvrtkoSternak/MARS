from difflib import SequenceMatcher
from math import sqrt


class Variable:
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("Variable {", self.value, "}")

    def unparse(self, num_tabs):
        print(self.value, end = '')

    def walk(self, postorder = False):
        return [self]

    def reconstruct(self, tree):
        return self

    def is_leaf(self):
        return True

    def similarity(self, node):
        if not isinstance(node, self.__class__):
            return 0
        else:
            s = SequenceMatcher(None, self.value, node.value)
            return s.ratio()


class Constant:
    def __init__(self, value, type_of):
        self.value = value
        self.type_of = type_of

    def print_me(self):
        print("Constant {", self.type_of, " ", self.value, " }")

    def unparse(self, num_tabs):
        print(self.value, end='')

    def walk(self, postorder = False):
        return [self]

    def reconstruct(self, tree):
        return self

    def is_leaf(self):
        return True

    def similarity(self, node):
        if not isinstance(node, self.__class__):
            return 0
        if not self.type_of == node.type_of:
            return 0
        else:
            s = SequenceMatcher(None, self.value, node.value)
            return s.ratio()


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

    def walk(self, postorder = False):
        tree = list()
        if not postorder:
            tree.append(self)
        tree.extend(self.variable.walk(postorder=postorder))
        tree.extend(self.value.walk(postorder=postorder))
        if postorder:
            tree.append(self)
        return tree

    def reconstruct(self, tree):
        self.variable = tree.pop(0).reconstruct(tree)
        self.value = tree.pop(0).reconstruct(tree)
        return self

    def is_leaf(self):
        return False

    def similarity(self, node, node_pairs):
        if not isinstance(node, self.__class__):
            return 0
        if self.operation != node.operation:
            return 0
        else:
            node_sim = node_pairs.get((self.value, node.value), 0) + node_pairs.get((self.variable, node.variable), 0)
            node_sim /= 2
            return sqrt(node_sim)

    def get_children(self, node):
        children = list()
        children.append(node.variable)
        children.append(node.value)
        return children


class FunctionName:
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("FunctionName {", self.value, "}")

    def unparse(self, num_tabs):
        print("{0}(".format(self.value), end='')

    def walk(self, postorder = False):
        return [self]

    def reconstruct(self, tree):
        return self

    def is_leaf(self):
        return True

    def similarity(self, node):
        if not isinstance(node, self.__class__):
            return 0
        else:
            s = SequenceMatcher(None, self.value, node.value)
            return s.ratio()


class Function:
    def __init__(self, args, value):
        self.start = Startnode()
        self.end = Endnode()
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

    def walk(self, postorder = False):
        tree = list()
        if not postorder:
            tree.append(self)
        tree.append(self.start)
        tree.extend(self.value.walk(postorder=postorder))
        for arg in self.args:
            tree.extend(arg.walk(postorder=postorder))
        tree.append(self.end)
        if postorder:
            tree.append(self)
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

    def is_leaf(self):
        return False

    def similarity(self, node, node_pairs):
        if not isinstance(node, self.__class__):
            return 0
        else:
            func_name_sim = node_pairs.get((self.value, node.value), 0)
            arg_sim = 0
            num_keys = 0
            for self_arg in self.args:
                for node_arg in node.args:
                    if (self_arg, node_arg) in node_pairs:
                        num_keys += 1
                        arg_sim += node_pairs.get((self_arg, node_arg), 0)
            arg_sim = arg_sim / max(num_keys, max(len(self.args), len(node.args)), 1)

            return (func_name_sim + arg_sim) / 2

    def get_children(self, node):
        children = list()
        children.append(node.start)
        children.append(node.value)
        children.extend(node.args)
        children.append(node.end)
        return children


class Condition:
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("Condition {")
        self.value.print_me()
        print("}")

    def unparse(self, num_tabs):
        self.value.unparse(num_tabs)

    def walk(self, postorder = False):
        tree = list()
        if not postorder:
            tree.append(self)
        tree.extend(self.value.walk(postorder = postorder))
        if postorder:
            tree.append(self)
        return tree

    def reconstruct(self, tree):
        self.value = tree.pop(0).reconstruct(tree)
        return self

    def is_leaf(self):
        return False

    def similarity(self, node, node_pairs):
        if not isinstance(node, self.__class__):
            return 0
        else:
            return node_pairs.get((self.value, node.value), 0)

    def get_children(self, node):
        children = list()
        children.append(node.value)
        return children


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

    def walk(self, postorder = False):
        tree = list()
        if not postorder:
            tree.append(self)
        tree.extend(self.condition.walk(postorder = postorder))
        tree.extend(self.body.walk(postorder = postorder))
        tree.extend(self.next_if.walk(postorder = postorder))
        if postorder:
            tree.append(self)
        return tree

    def reconstruct(self, tree):
        self.condition = tree.pop(0).reconstruct(tree)
        self.body = tree.pop(0).reconstruct(tree)
        self.next_if = tree.pop(0).reconstruct(tree)
        return self

    def is_leaf(self):
        return False

    def similarity(self, node, node_pairs):
        if not isinstance(node, self.__class__):
            return 0
        else:
            cond_sim = node_pairs.get((self.condition, node.condition), 0)
            body_sim = node_pairs.get((self.body, node.body), 0)
            elif_sim = node_pairs.get((self.next_if, node.next_if), 0)
            return (2*cond_sim + body_sim + elif_sim) / 4

    def get_children(self, node):
        children = list()
        children.append(node.condition)
        children.append(node.body)
        children.append(node.next_if)
        return children


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

    def walk(self, postorder = False):
        tree = list()
        if not postorder:
            tree.append(self)
        tree.extend(self.body.walk(postorder = postorder))
        if postorder:
            tree.append(self)
        return tree

    def reconstruct(self, tree):
        self.body = tree.pop(0).reconstruct(tree)
        return self

    def is_leaf(self):
        return False

    def similarity(self, node, node_pairs):
        if not isinstance(node, self.__class__):
            return 0
        else:
            return node_pairs.get((self.body, node.body), 0)

    def get_children(self, node):
        children = list()
        children.append(node.body)
        return children


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

    def walk(self, postorder = False):
        tree = list()
        if not postorder:
            tree.append(self)
        tree.extend(self.condition.walk(postorder = postorder))
        tree.extend(self.body.walk(postorder = postorder))
        tree.extend(self.next_if.walk(postorder = postorder))
        if postorder:
            tree.append(self)
        return tree

    def reconstruct(self, tree):
        self.condition = tree.pop(0).reconstruct(tree)
        self.body = tree.pop(0).reconstruct(tree)
        self.next_if = tree.pop(0).reconstruct(tree)
        return self

    def is_leaf(self):
        return False

    def similarity(self, node, node_pairs):
        if not isinstance(node, self.__class__):
            return 0
        else:
            cond_sim = node_pairs.get((self.condition, node.condition), 0)
            body_sim = node_pairs.get((self.body, node.body), 0)
            elif_sim = node_pairs.get((self.next_if, node.next_if), 0)
            return (2*cond_sim + body_sim + elif_sim) / 4

    def get_children(self, node):
        children = list()
        children.append(node.condition)
        children.append(node.body)
        children.append(node.next_if)
        return children


class Body:
    def __init__(self, children):
        self.start = Startnode()
        self.children = children
        self.end = Endnode()

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

    def walk(self, postorder = False):
        tree = list()
        if not postorder:
            tree.append(self)
        tree.append(self.start)
        for child in self.children:
            tree.extend(child.walk(postorder = postorder))
        tree.append(self.end)
        if postorder:
            tree.append(self)
        return tree

    def reconstruct(self, tree):
        self.children.clear()
        tree.pop(0)
        child = tree.pop(0)
        while not isinstance(child, Endnode):
            self.children.append(child.reconstruct(tree))
            child = tree.pop(0)
        return self

    def is_leaf(self):
        return False

    def similarity(self, node, node_pairs):
        if not isinstance(node, self.__class__):
            return 0
        else:
            children_sim = 0
            num_keys = 0
            for self_child in self.children:
                for node_child in node.children:
                    if (self_child, node_child) in node_pairs:
                        num_keys += 1
                        children_sim += node_pairs.get((self_child, node_child), 0)

            return children_sim / max(num_keys, max(len(self.children), len(node.children)), 1)

    def get_children(self, node):
        children = list()
        children.append(node.start)
        children.extend(node.children)
        children.append(node.end)
        return children


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

    def walk(self, postorder = False):
        tree = list()
        if not postorder:
            tree.append(self)
        tree.extend(self.first.walk(postorder = postorder))
        tree.extend(self.operation.walk(postorder = postorder))
        tree.extend(self.second.walk(postorder = postorder))
        if postorder:
            tree.append(self)
        return tree

    def reconstruct(self, tree):
        self.first = tree.pop(0).reconstruct(tree)
        self.operation = tree.pop(0).reconstruct(tree)
        self.second = tree.pop(0).reconstruct(tree)
        return self

    def is_leaf(self):
        return False

    def similarity(self, node, node_pairs):
        if not isinstance(node, self.__class__) \
                or not isinstance(node, UnaryOperation) \
                or not isinstance(node, Compare):
            return 0
        else:
            first_sim = node_pairs.get((self.first, node.first), 0)
            second_sim = node_pairs.get((self.second, node.second), 0)
            op_sim = node_pairs.get((self.operation, node.operation), 0)
            return (2*op_sim + first_sim + second_sim) / 4

    def get_children(self, node):
        children = list()
        children.append(node.first)
        children.append(node.second)
        children.append(node.operation)
        return children


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

    def walk(self, postorder = False):
        tree = list()
        if not postorder:
            tree.append(self)
        tree.extend(self.operation.walk(postorder = postorder))
        tree.extend(self.first.walk(postorder = postorder))
        if postorder:
            tree.append(self)
        return tree

    def reconstruct(self, tree):
        self.operation = tree.pop(0).reconstruct(tree)
        self.first = tree.pop(0).reconstruct(tree)
        return self

    def is_leaf(self):
        return False

    def similarity(self, node, node_pairs):
        if not isinstance(node, self.__class__) \
                or not isinstance(node, BoolOperation)\
                or not isinstance(node, Compare):
            return 0
        else:
            first_sim = node_pairs.get((self.first, node.first), 0)
            op_sim = node_pairs.get((self.operation, node.operation), 0)
            return (1.5*op_sim + first_sim) / 2.5

    def get_children(self, node):
        children = list()
        children.append(node.first)
        children.append(node.operation)
        return children


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

    def walk(self, postorder = False):
        tree = list()
        if not postorder:
            tree.append(self)
        tree.extend(self.first.walk(postorder = postorder))
        tree.extend(self.operation.walk(postorder = postorder))
        tree.extend(self.second.walk(postorder = postorder))
        if postorder:
            tree.append(self)
        return tree

    def reconstruct(self, tree):
        self.first = tree.pop(0).reconstruct(tree)
        self.operation = tree.pop(0).reconstruct(tree)
        self.second = tree.pop(0).reconstruct(tree)
        return self

    def is_leaf(self):
        return False

    def similarity(self, node, node_pairs):
        if not isinstance(node, self.__class__) \
                or not isinstance(node, BoolOperation) \
                or not isinstance(node, UnaryOperation):
            return 0
        else:
            first_sim = node_pairs.get((self.first, node.first), 0)
            second_sim = node_pairs.get((self.second, node.second), 0)
            op_sim = node_pairs.get((self.operation, node.operation), 0)
            return (2*op_sim + first_sim + second_sim) / 4

    def get_children(self, node):
        children = list()
        children.append(node.first)
        children.append(node.second)
        children.append(node.operation)
        return children


class EmptyNode:
    def print_me(self):
        pass

    def unparse(self, num_tabs):
        pass

    def walk(self, postorder = False):
        return [self]

    def reconstruct(self, tree):
        return self

    def is_leaf(self):
        return True

    def similarity(self, node):
        if not isinstance(node, self.__class__):
            return 0
        else:
            return 1


class Startnode:
    def print_me(self):
        print("Start Node")

    def unparse(self, num_tabs):
        pass

    def walk(self, postorder = False):
        return [self]

    def reconstruct(self, tree):
        return self

    def is_leaf(self):
        return True

    def similarity(self, node):
        if not isinstance(node, self.__class__):
            return 0
        else:
            return 0.5


class Endnode:
    def print_me(self):
        print("End Node")

    def unparse(self, num_tabs):
        pass

    def walk(self, postorder = False):
        return [self]

    def reconstruct(self, tree):
        return self

    def is_leaf(self):
        return True

    def similarity(self, node):
        if not isinstance(node, self.__class__):
            return 0
        else:
            return 0.5

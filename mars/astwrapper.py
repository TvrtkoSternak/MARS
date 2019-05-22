from abc import abstractmethod
from difflib import SequenceMatcher
from math import sqrt


class Node:

    @abstractmethod
    def print_me(self):
        pass

    @abstractmethod
    def unparse(self, num_tabs):
        pass

    @abstractmethod
    def to_source_code(self, num_tabs):
        pass

    @abstractmethod
    def walk(self, postorder = False):
        pass

    @abstractmethod
    def reconstruct(self, tree):
        pass

    @abstractmethod
    def is_leaf(self):
        pass

    @abstractmethod
    def similarity(self, node):
        pass

    @abstractmethod
    def is_mutable(self, node):
        pass

    def num_children(self):
        return len(self.get_all_children())

    @abstractmethod
    def get_all_children(self):
        pass

    @abstractmethod
    def get_children(self, node):
        pass

    @abstractmethod
    def equals(self, other):
        pass


class Leaf(Node):

    @abstractmethod
    def print_me(self):
        pass

    @abstractmethod
    def unparse(self, num_tabs):
        pass

    @abstractmethod
    def to_source_code(self, num_tabs):
        pass

    def walk(self, postorder = False):
        return [self]

    def reconstruct(self, tree):
        return self

    def is_leaf(self):
        return True

    @abstractmethod
    def similarity(self, node):
        pass

    def is_mutable(self, node):
        return True

    def get_all_children(self):
        return list()

    def get_children(self, node):
        return list()

    @abstractmethod
    def equals(self, other):
        pass


class Variable(Leaf):
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("Variable {", self.value, "}")

    def unparse(self, num_tabs):
        print(self.value, end = '')

    def to_source_code(self, num_tabs):
        return str(self.value)

    def similarity(self, node):
        if not isinstance(node, self.__class__):
            return 0
        else:
            s = SequenceMatcher(None, self.value, node.value)
            return (2*s.ratio() + 1)/3

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.value == self.value
        return False


class Constant(Leaf):
    def __init__(self, value, type_of):
        self.value = value
        self.type_of = type_of

    def print_me(self):
        print("Constant {", self.type_of, " ", self.value, " }")

    def unparse(self, num_tabs):
        print(self.value, end='')

    def to_source_code(self, num_tabs):
        return str(self.value)

    def similarity(self, node):
        if not isinstance(node, self.__class__):
            return 0
        if not self.type_of == node.type_of:
            return 0
        else:
            s = SequenceMatcher(None, str(self.value), str(node.value))
            return s.ratio()

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.value == self.value \
                   and other.type_of == self.type_of
        return False


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

    def to_source_code(self, num_tabs):
        return ' '.join([
            self.variable.to_source_code(num_tabs),
            str(self.operation),
            self.value.to_source_code(num_tabs)
        ])

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

    def is_mutable(self, node):
        if isinstance(node, self.__class__):
            return True
        else:
            return False

    def num_children(self):
        return 2 + self.variable.num_children() + self.value.num_children()

    def get_all_children(self):
        children = list()
        children.append(self.variable)
        children.extend(self.variable.get_all_children())
        children.append(self.value)
        children.extend(self.value.get_all_children())
        return children

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.operation == self.operation \
                   and other.value.equals(self.value) \
                   and other.variable.equals(self.variable)
        return False


class FunctionName(Leaf):
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("FunctionName {", self.value, "}")

    def unparse(self, num_tabs):
        print("{0}".format(self.value), end='')

    def to_source_code(self, num_tabs):
        return str(self.value)

    def similarity(self, node):
        if not isinstance(node, self.__class__):
            return 0
        else:
            s = SequenceMatcher(None, self.value, node.value)
            return s.ratio()

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.value == self.value
        return False


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
        print("(", end='')
        if self.args:
            if len(self.args) != 1:
                index = 0
                while index < len(self.args) - 1:
                    self.args[index].unparse(num_tabs)
                    print(", ", end='')
                    index += 1
            self.args[-1].unparse(num_tabs)
        print(")", end='')

    def to_source_code(self, num_tabs):
        str_list = list()
        str_list.append(self.value.to_source_code(num_tabs))
        str_list.append('(')
        if self.args:
            if len(self.args) != 1:
                index = 0
                while index < len(self.args) - 1:
                    str_list.append(self.args[index].to_source_code(num_tabs))
                    str_list.append(", ")
                    index += 1
            str_list.append(self.args[-1].to_source_code(num_tabs))
        str_list.append(")")
        return ''.join(str_list)

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

    def is_mutable(self, node):
        if isinstance(node, self.__class__):
            return True
        else:
            return False

    def num_children(self):
        num_children = 3
        for arg in self.args:
            num_children += arg.num_children() + 1
        return num_children + self.value.num_children()

    def get_all_children(self):
        children = list()
        for arg in self.args:
            children.append(arg)
            children.extend(arg.get_all_children())
        children.append(self.value)
        children.extend(self.value.get_all_children())
        return children

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if not isinstance(other, self.__class__):
            return False
        if not other.value.equals(self.value):
            return False
        if len(other.args) != len(self.args):
            if any(isinstance(x, Wildcard) for x in other.children):
                return True
            if any(isinstance(x, Wildcard) for x in self.children):
                return True
            return False
        for other_arg, self_arg in zip(other.args, self.args):
            if not other_arg.equals(self_arg):
                return False
        return True


class Condition:
    def __init__(self, value):
        self.value = value

    def print_me(self):
        print("Condition {")
        self.value.print_me()
        print("}")

    def unparse(self, num_tabs):
        self.value.unparse(num_tabs)

    def to_source_code(self, num_tabs):
        return self.value.to_source_code(num_tabs)

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
        if not isinstance(node, self.__class__) \
                and not isinstance(node, Compare)\
                and not isinstance(node, BoolOperation)\
                and not isinstance(node, UnaryOperation):
            return 0
        elif isinstance(node, Condition):
            return node_pairs.get((self.value, node.value), 0)
        else:
            return 0.3

    def get_children(self, node):
        children = list()
        children.append(node.value)
        return children

    def is_mutable(self, node):
        if isinstance(node, self.__class__):
            return True
        else:
            return False

    def num_children(self):
        return 1 + self.value.num_children()

    def get_all_children(self):
        children = list()
        children.append(self.value)
        children.extend(self.value.get_all_children())
        return children

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.value.equals(self.value)
        return False


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

    def to_source_code(self, num_tabs):
        return ''.join([
            "\t"*num_tabs + "elif ",
            self.condition.to_source_code(num_tabs),
            ":\n",
            self.body.to_source_code(num_tabs + 1),
            self.next_if.to_source_code(num_tabs)
        ])

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

    def is_mutable(self, node):
        if isinstance(node, self.__class__):
            return True
        else:
            return False

    def num_children(self):
        return 3 + self.condition.num_children() + self.body.num_children() + self.next_if.num_children()

    def get_all_children(self):
        children = list()
        children.append(self.condition)
        children.extend(self.condition.get_all_children())
        children.append(self.body)
        children.extend(self.body.get_all_children())
        children.append(self.next_if)
        children.extend(self.next_if.get_all_children())
        return children

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.condition.equals(self.condition) \
                   and other.body.equals(self.body) \
                   and other.next_if.equals(self.next_if)
        return False


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

    def to_source_code(self, num_tabs):
        return self.body.to_source_code(num_tabs)

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

    def is_mutable(self, node):
        if isinstance(node, self.__class__):
            return True
        else:
            return False

    def num_children(self):
        return 1 + self.body.num_children()

    def get_all_children(self):
        children = list()
        children.append(self.body)
        children.extend(self.body.get_all_children())
        return children

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.body.equals(self.body)
        return False


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

    def to_source_code(self, num_tabs):
        return ''.join([
            "if ",
            self.condition.to_source_code(num_tabs),
            ":\n",
            self.body.to_source_code(num_tabs + 1),
            self.next_if.to_source_code(num_tabs)
        ])

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

    def is_mutable(self, node):
        if isinstance(node, self.__class__):
            return True
        else:
            return False

    def num_children(self):
        return 3 + self.condition.num_children() + self.body.num_children() + self.next_if.num_children()

    def get_all_children(self):
        children = list()
        children.append(self.condition)
        children.extend(self.condition.get_all_children())
        children.append(self.body)
        children.extend(self.body.get_all_children())
        children.append(self.next_if)
        children.extend(self.next_if.get_all_children())
        return children

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.condition.equals(self.condition) \
                   and other.body.equals(self.body) \
                   and other.next_if.equals(self.next_if)
        return False


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

    def to_source_code(self, num_tabs):
        str_list = []
        for child in self.children:
            str_list.append("\t"*num_tabs)
            str_list.append(child.to_source_code(num_tabs))
            if not hasattr(child, 'body'):
                str_list.append("\n")
        return ''.join(str_list)

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

    def is_mutable(self, node):
        if isinstance(node, self.__class__):
            return True
        else:
            return False

    def num_children(self):
        num_children = 2
        for child in self.children:
            num_children += child.num_children() + 1
        return num_children

    def get_all_children(self):
        children = list()
        for child in self.children:
            children.append(child)
            children.extend(child.get_all_children())
        return children

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if not isinstance(other, self.__class__):
            return False
        if len(other.children) != len(self.children):
            if any(isinstance(x, Wildcard) for x in other.children):
                return True
            if any(isinstance(x, Wildcard) for x in self.children):
                return True
            return False
        for other_children, self_children in zip(other.children, self.children):
            if not other_children.equals(self_children):
                return False
        return True


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

    def to_source_code(self, num_tabs):
        return ''.join([
            self.first.to_source_code(num_tabs),
            self.operation.to_source_code(num_tabs),
            self.second.to_source_code(num_tabs)
        ])

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
                and not isinstance(node, UnaryOperation) \
                and not isinstance(node, Compare)\
                and not isinstance(node, Condition):
            return 0
        elif isinstance(node, Condition):
            return 0.3
        elif isinstance(node, UnaryOperation):
            first_sim = node_pairs.get((self.first, node.first), 0)
            return first_sim**2
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

    def is_mutable(self, node):
        if isinstance(node, self.__class__):
            return True
        else:
            return False

    def num_children(self):
        return 3 + self.first.num_children() + self.operation.num_children() + self.second.num_children()

    def get_all_children(self):
        children = list()
        children.append(self.first)
        children.extend(self.first.get_all_children())
        children.append(self.second)
        children.extend(self.second.get_all_children())
        children.append(self.operation)
        children.extend(self.operation.get_all_children())
        return children

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.operation.equals(self.operation) \
                   and other.second.equals(self.second) \
                   and other.first.equals(self.first)
        return False


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

    def to_source_code(self, num_tabs):
        return ''.join([
            self.operation.to_source_code(num_tabs),
            self.first.to_source_code(num_tabs)
        ])

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
                and not isinstance(node, BoolOperation)\
                and not isinstance(node, Compare)\
                and not isinstance(node, Condition):
            return 0
        elif isinstance(node, Condition):
            return 0.3
        else:
            first_sim = node_pairs.get((self.first, node.first), 0)
            op_sim = node_pairs.get((self.operation, node.operation), 0)
            return (1.5*op_sim + first_sim) / 2.5

    def get_children(self, node):
        children = list()
        children.append(node.first)
        children.append(node.operation)
        return children

    def is_mutable(self, node):
        if isinstance(node, self.__class__):
            return True
        else:
            return False

    def num_children(self):
        return 2 + self.first.num_children() + self.operation.num_children()

    def get_all_children(self):
        children = list()
        children.append(self.first)
        children.extend(self.first.get_all_children())
        children.append(self.operation)
        children.extend(self.operation.get_all_children())
        return children

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.operation.equals(self.operation) \
                   and other.first.equals(self.first)
        return False


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

    def to_source_code(self, num_tabs):
        return ''.join([
            self.first.to_source_code(num_tabs),
            self.operation.to_source_code(num_tabs),
            self.second.to_source_code(num_tabs)
        ])

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
                and not isinstance(node, BoolOperation) \
                and not isinstance(node, UnaryOperation)\
                and not isinstance(node, Condition):
            return 0
        elif isinstance(node, Condition):
            return 0.3
        elif isinstance(node, UnaryOperation):
            first_sim = node_pairs.get((self.first, node.first), 0)
            return first_sim**2
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

    def is_mutable(self, node):
        if isinstance(node, self.__class__):
            return True
        else:
            return False

    def num_children(self):
        return 3 + self.first.num_children() + self.operation.num_children() + self.second.num_children()

    def get_all_children(self):
        children = list()
        children.append(self.first)
        children.extend(self.first.get_all_children())
        children.append(self.second)
        children.extend(self.second.get_all_children())
        children.append(self.operation)
        children.extend(self.operation.get_all_children())
        return children

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.operation.equals(self.operation) \
                   and other.second.equals(self.second) \
                   and other.first.equals(self.first)
        return False


class While(Node):

    def __init__(self, test, body):
        self.test = test
        self.body = body

    def unparse(self, num_tabs):
        print("while ", end='')
        self.test.unparse(num_tabs)
        print(":")
        self.body.unparse(num_tabs + 1)

    def to_source_code(self, num_tabs):
        return ''.join([
            "while ",
            self.test.to_source_code(num_tabs),
            ":\n",
            self.body.to_source_code(num_tabs + 1)
        ])

    def walk(self, postorder=False):
        tree = list()
        if not postorder:
            tree.append(self)
        tree.extend(self.test.walk(postorder=postorder))
        tree.extend(self.body.walk(postorder=postorder))
        if postorder:
            tree.append(self)
        return tree

    def reconstruct(self, tree):
        self.test = tree.pop(0).reconstruct(tree)
        self.body = tree.pop(0).reconstruct(tree)
        return self

    def is_leaf(self):
        return False

    def similarity(self, node, node_pairs):
        if not isinstance(node, self.__class__) \
                and not isinstance(node, For):
            return 0
        elif isinstance(node, For):
            body_sim = node_pairs.get((self.body, node.body), 0)
            return (body_sim + 0.5) / 2
        else:
            test_sim = node_pairs.get((self.test, node.test), 0)
            body_sim = node_pairs.get((self.body, node.body), 0)
            return (2 * test_sim + body_sim ) / 3

    def is_mutable(self, node):
        if isinstance(node, self.__class__):
            return True
        else:
            return False

    def get_all_children(self):
        children = list()
        children.append(self.test)
        children.extend(self.test.get_all_children())
        children.append(self.body)
        children.extend(self.body.get_all_children())
        return children

    def get_children(self, node):
        children = list()
        children.append(node.test)
        children.append(node.body)
        return children

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.test.equals(self.test) \
                   and other.body.equals(self.body)
        return False

    def print_me(self):
        print("While")


class For(Node):

    def __init__(self, target, iter, body):
        self.target = target
        self.iter = iter
        self.body = body

    def unparse(self, num_tabs):
        print("for ", end='')
        self.target.unparse(num_tabs)
        print(" in ", end='')
        self.iter.unparse(num_tabs)
        print(":")
        self.body.unparse(num_tabs + 1)

    def to_source_code(self, num_tabs):
        return ''.join([
            "for ",
            self.target.to_source_code(num_tabs),
            " in ",
            self.iter.to_source_code(num_tabs),
            ":\n",
            self.body.to_source_code(num_tabs + 1)
        ])

    def walk(self, postorder=False):
        tree = list()
        if not postorder:
            tree.append(self)
        tree.extend(self.target.walk(postorder=postorder))
        tree.extend(self.iter.walk(postorder=postorder))
        tree.extend(self.body.walk(postorder=postorder))
        if postorder:
            tree.append(self)
        return tree

    def reconstruct(self, tree):
        self.target = tree.pop(0).reconstruct(tree)
        self.iter = tree.pop(0).reconstruct(tree)
        self.body = tree.pop(0).reconstruct(tree)
        return self

    def is_leaf(self):
        return False

    def similarity(self, node, node_pairs):
        if not isinstance(node, self.__class__) \
                and not isinstance(node, While):
            return 0
        elif isinstance(node, While):
            body_sim = node_pairs.get((self.body, node.body), 0)
            return (body_sim + 0.5) / 2
        else:
            target_sim = node_pairs.get((self.target, node.target), 0)
            iter_sim = node_pairs.get((self.iter, node.iter), 0)
            body_sim = node_pairs.get((self.body, node.body), 0)
            return (2 * iter_sim + body_sim + target_sim) / 4

    def is_mutable(self, node):
        if isinstance(node, self.__class__):
            return True
        else:
            return False

    def get_all_children(self):
        children = list()
        children.append(self.target)
        children.extend(self.target.get_all_children())
        children.append(self.iter)
        children.extend(self.iter.get_all_children())
        children.append(self.body)
        children.extend(self.body.get_all_children())
        return children

    def get_children(self, node):
        children = list()
        children.append(node.target)
        children.append(node.iter)
        children.append(node.body)
        return children

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return other.target.equals(self.target) \
                   and other.body.equals(self.body) \
                   and other.iter.equals(self.iter)
        return False

    def print_me(self):
        print("For")


class EmptyNode(Leaf):
    def print_me(self):
        pass

    def unparse(self, num_tabs):
        pass

    def to_source_code(self, num_tabs):
        return ""

    def similarity(self, node):
        if not isinstance(node, self.__class__):
            return 0
        else:
            return 1

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return True
        return False


class Startnode(Leaf):
    def print_me(self):
        print("Start Node")

    def unparse(self, num_tabs):
        pass

    def to_source_code(self, num_tabs):
        return ""

    def similarity(self, node):
        if not isinstance(node, self.__class__):
            return 0
        else:
            return 0.5

    def is_mutable(self, node):
        return False

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return True
        return False


class Endnode(Leaf):
    def print_me(self):
        print("End Node")

    def unparse(self, num_tabs):
        pass

    def to_source_code(self, num_tabs):
        return ""

    def similarity(self, node):
        if not isinstance(node, self.__class__):
            return 0
        else:
            return 0.5

    def is_mutable(self, node):
        return False

    def equals(self, other):
        if isinstance(other, Wildcard):
            return True
        if isinstance(other, self.__class__):
            return True
        return False


class Wildcard(Leaf):

    def __init__(self, wrapped_node, type):
        self.wrapped_node = wrapped_node
        self.type = type
        self.index = 0

    def print_me(self):
        print("Wildcard {", self.index, "}")

    def unparse(self, num_tabs):
        print("Wildcard(", self.index, ")", sep='', end='')

    def to_source_code(self, num_tabs):
        return "Wildcard(" + str(self.index) + ")"

    def similarity(self, node):
        if isinstance(node, Use):
            if node.index == self.index:
                return 1.0
        return 0.5

    def equals(self, other):
        return True


class Use(Leaf):

    def __init__(self, wrapped_node, type):
        self.wrapped_node = wrapped_node
        self.type = type
        self.index = 0

    def print_me(self):
        print("Use {", self.index, "}")

    def unparse(self, num_tabs):
        print("Use(", self.index, ")", sep='', end='')

    def to_source_code(self, num_tabs):
        return "Use(" + str(self.index) + ")"

    def similarity(self, node):
        if isinstance(node, Wildcard):
            if node.index == self.index:
                return 1.0
        return 0.5

    def equals(self, other):
        return True



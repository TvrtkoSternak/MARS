import _ast
import ast


class AstUtils:

    @staticmethod
    def is_leaf(node):
        if node.__class__ is _ast.Name:
            return True
        for _ in ast.iter_child_nodes(node):
            return False
        return True

        #return not hasattr(node, "body")

    @staticmethod
    def walk_all_nodes(node):
        nodes = []
        AstUtils.recursive(node, nodes, 0, None, 0)
        return nodes

    @staticmethod
    def recursive(node, nodes, level, parent, index):
        if not AstUtils.is_leaf(node):
            detailed_node = DetailedNode(False, node, level, parent, index)

            nodes += [detailed_node]

            for child in ast.iter_child_nodes(node):
                child_node, index = AstUtils.recursive(child, nodes, level+1, detailed_node, index + 1)
                if child_node is not None:
                    detailed_node.children += [child_node]

            return detailed_node, index

        else:
            detailed_node = DetailedNode(True, node, level, parent, index)
            nodes += [detailed_node]
            if node.__class__ is _ast.Name:
                index += 1
            return detailed_node, index

    @staticmethod
    def change_to_postorder(node, postorder_list):
        for child in node.children:
            AstUtils.change_to_postorder(child, postorder_list)
        postorder_list += [node]


class DetailedNode:

    def __init__(self, leaf, node, level, parent, index):
        self.leaf = leaf
        self.node = node
        self.level = level
        self.parent = parent
        self.index = index
        self.children = []
        self.matched = False

    def get_value(self):
        value = ""
        if self.node.__class__ is _ast.Assign:
            return self.node.targets[0].id.__str__() + '=' + self.node.value.n.__str__()
        elif self.node.__class__ is _ast.Expr:
            return self.node.value.func.id.__str__() + self.node.value.args[0].s.__str__()
        elif self.node.__class__ is _ast.Compare:
            if self.node.ops[0].__class__ is _ast.Gt:
                return self.node.left.id.__str__() + '>' + self.node.comparators[0].n.__str__()
        for child in ast.iter_child_nodes(self.node):
            if hasattr(child, 'id'):
                value += child.id
            elif hasattr(child, 's'):
                value += child.s.__str__()
            elif hasattr(child, 'n'):
                value += child.n.__str__()
            else:
                value += child.__str__()
        return value

    def __str__(self):
        return self.node.__str__() + '; isLeaf: ' + self.leaf.__str__() + '; level: ' + self.level.__str__()

    def number_of_children(self):
        count = 0
        for child in self.children:
            count += child.count_recursive()
        return count

    def count_recursive(self):
        if self.leaf:
            return 1
        else:
            count = 0
            for child in self.children:
                count += DetailedNode.count_recursive(child)
            return count

    def number_of_direct_children(self):
        return self.children.__len__()


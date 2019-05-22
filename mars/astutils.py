import _ast
import ast

from mars.astwrapper import Body, Function, Constant, If, Variable, EmptyNode, Condition, BoolOperation, Compare, \
    UnaryOperation, Assign, ElIf, Else, FunctionName, While, For


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

    @staticmethod
    def find_functions(node):
        finder = FunctionFinder()
        finder.generic_visit(node)
        return finder.context


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
            if self.node.value.__class__ is _ast.Call:
                return self.node.targets[0].id.__str__() + '=' + self.node.value.func.id
            return self.node.targets[0].id.__str__() + '=' + self.node.value.n.__str__()
        # elif self.node.__class__ is _ast.Expr:
        #     return self.node.value.func.id.__str__() + self.node.value.args[0].s.__str__()
        elif self.node.__class__ is _ast.Compare:
            if self.node.ops[0].__class__ is _ast.Gt:
                return self.node.left.id.__str__() + '>' + self.node.comparators[0].n.__str__()
        elif self.node.__class__ is _ast.Num:
            return "@" + self.node.n.__str__()
        elif self.node.__class__ is _ast.Name:
            return "@" + self.node.id
        elif self.node.__class__ is _ast.Gt:
            return '>'
        elif self.node.__class__ is _ast.Str:
            return 'str'
            # return self.node.s
        elif self.node.__class__ is _ast.Module:
            return 'Module'
        elif self.node.__class__ is _ast.If:
            return 'If node at ' + self.index.__str__()
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

    def number_of_children(self, count_inner_nodes=False):
        count = 0
        for child in self.children:
            count += child.count_recursive(count_inner_nodes)
        return count

    def count_recursive(self, count_inner_nodes):
        if self.leaf:
            if self.node.__class__ is _ast.Name:
                return 2
            if self.node.__class__ is _ast.Call:
                return 3
            return 1
        else:
            count = 0
            for child in self.children:
                count += child.count_recursive(count_inner_nodes)
            return count if count_inner_nodes else count + 1

    def number_of_direct_children(self):
        return self.children.__len__()

    def __eq__(self, other):
        if other.__class__ is not DetailedNode:
            return False
        if other.node.__class__ is not self.node.__class__:
            return False
        if self.leaf:
            if self.get_value() != other.get_value():
                return False
        if other.node.__class__ is _ast.Call:
            # print(other.node.func)
            return other.node.func.id == self.node.func.id
        return True


class FunctionFinder(ast.NodeVisitor):
    def __init__(self):
        self.context = dict()
        self.current_class = 'no_class'
        self.context[self.current_class] = dict()

    def visit_FunctionDef(self, node):
        self.context[self.current_class][node.name] = node
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.context[node.name] = dict()
        self.generic_visit(node)


class AstWrapper(ast.NodeTransformer):
    def __init__(self):
        pass

    def visit_Module(self, node):
        children = list()
        for child in node.body:
            children.append(self.visit(child))
        return Body(children)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Call(self, node):
        args = list()
        for arg in node.args:
            args.append(self.visit(arg))
        function = Function(args, FunctionName(node.func.id))
        return function

    def visit_Name(self, node):
        return Variable(node.id)

    def visit_Num(self, node):
        return Constant(node.n, "NUMBER")

    def visit_Str(self, node):
        value = ["\"", node.s, "\""]
        return Constant("".join(value), "STRING")

    def visit_Compare(self, node):
        return Compare(self.visit(node.ops[0]), self.visit(node.left), self.visit(node.comparators[0]))

    def visit_BoolOp(self, node):
        return BoolOperation(self.visit(node.op), self.visit(node.values[0]), self.visit(node.values[1]))

    def visit_UnaryOp(self, node):
        return UnaryOperation(self.visit(node.op), self.visit(node.operand))

    def visit_Not(self, node):
        return Constant(" not ", "UNARYOP")

    def visit_Is(self, node):
        return Constant(" is ", "CMPOP")

    def visit_In(self, node):
        return Constant(" in ", "CMPOP")

    def visit_NameConstant(self, node):
        return Constant(node.value, "CONSTANT")

    def visit_NotIn(self, node):
        return Constant(" not in ", "CMPOP")

    def visit_Eq(self, node):
        return Constant(" == ", "CMPOP")

    def visit_NotEq(self, node):
        return Constant(" != ", "CMPOP")

    def visit_Lt(self, node):
        return Constant(" < ", "CMPOP")

    def visit_LtE(self, node):
        return Constant(" <= ", "CMPOP")

    def visit_Gt(self, node):
        return Constant(" > ", "CMPOP")

    def visit_GtE(self, node):
        return Constant(" >= ", "CMPOP")

    def visit_IsNot(self, node):
        return Constant(" is not ", "CMPOP")

    def visit_And(self, node):
        return Constant(" and ", "BOOLOP")

    def visit_Or(self, node):
        return Constant(" or ", "BOOLOP")

    def visit_If(self, node):
        expressions = list()
        for expression in node.body:
            expressions.append(self.visit(expression))
        if node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                elif_node = self.visit(node.orelse[0])
                if_node = If(Condition(self.visit(node.test)), Body(expressions),
                             ElIf(elif_node.condition, elif_node.body, elif_node.next_if))
            else:
                else_expressions = list()
                for expression in node.orelse:
                    else_expressions.append(self.visit(expression))
                if_node = If(Condition(self.visit(node.test)), Body(expressions), Else(Body(else_expressions)))
        else:
            if_node = If(Condition(self.visit(node.test)), Body(expressions), EmptyNode())
        return if_node

    def visit_Assign(self, node):
        return Assign(self.visit(node.targets[0]), "=", self.visit(node.value))

    def visit_AugAssign(self, node):
        return Assign(self.visit(node.target), self.visit(node.op).value + "=", self.visit(node.value))

    def visit_Add(self, node):
        return Constant("+", "OPERATOR")

    def visit_Sub(self, node):
        return Constant("-", "OPERATOR")

    def visit_Mult(self, node):
        return Constant("*", "OPERATOR")

    def visit_Div(self, node):
        return Constant("/", "OPERATOR")

    def visit_While(self, node):
        expressions = list()
        for expression in node.body:
            expressions.append(self.visit(expression))

        return While(self.visit(node.test), Body(expressions))

    def visit_For(self, node):
        expressions = list()
        for expression in node.body:
            expressions.append(self.visit(expression))

        return For(self.visit(node.target), self.visit(node.iter), Body(expressions))

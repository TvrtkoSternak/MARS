import ast
import collections
from math import exp

from mars.astwrapper import Startnode, Endnode
from mars.pattern import EditScript, Pattern, Delete, Update, Insert


class PatternCreator:
    """
    A class that  is responsible for creating basic patterns from
    file inputs of original and modified code.

    ...

    Attributes
    ----------
    context : DbContext
        Context of a database used for saving created patterns
    ast_parser : ASTParser
        Object used to transform source-code into AST
    script_generator : EditScriptGenerator
        Object used to generate EditScript from original and modified code

    Methods
    -------
    public __init__(self, context)
        Initialises PatternCreator object.
    public Pattern create_pattern(self, original, modified)
        Creates a pattern from original and modified code files.
    public void save_pattern(self, created_pattern)
        Saves a pattern to a database in context attribute.
    """
    def __init__(self, differencer, ast_wrapper):
        """
        Initialises PatternCreator object.

        Parameters
        ----------
        context : DbContext
            Context of the database where the patterns will be saved
        ast_parser : ASTParser
            Object used to transform source-code into AST
        script_generator : EditScriptGenerator
            Object used to generate EditScript from original and modified code
        """
        self.differencer = differencer
        self.ast_wrapper = ast_wrapper

    def create_pattern(self, original_file, modified_file):
        """
        Creates a pattern from original and modified code files.

        Parameters
        ----------
        original : File
            File in which the original code is written
        Modified : File
            File in which the original code is written

        Returns
        -------
        Pattern
            Pattern object created from original and modified code
        """
        with open(original_file) as original:
            text_original = original.read()
        with open(modified_file) as modified:
            text_modified = modified.read()

        original_ast = self.ast_wrapper.visit(ast.parse(text_original))
        modified_ast = self.ast_wrapper.visit(ast.parse(text_modified))

        return Pattern(original_ast, modified_ast, self.differencer.connect_nodes(original_ast, modified_ast))


class EditScriptGenerator:
    """
    A class that is responsible for generating the EditScript object
    from ASTs of original and modified codes.

    ...

    Attributes
    ----------
    tree_differencer : TreeDifferencer
        Object that is responsible for connecting the same nodes in
        original and modified code ASTs

    Methods
    -------
    public __init__(self, tree_differencer)
        Initialises EditScriptGenerator object.
    public EditScript generate(self, original, modified)
        Generates an EditScript object from original and modified
        code ASTs that describes the modifications necessary to transform
        the original AST to modified AST.

    """
    def __init__(self, tree_differencer, sim_treshold):
        """
        Initialises EditScriptGenerator object

        Parameters
        ----------
        tree_differencer : TreeDifferencer
            Object that is responsible for connecting the same nodes in
            original and modified code ASTs
        """
        self.tree_differencer = tree_differencer
        self.sim_treshold = sim_treshold

    def generate(self, first_ast, second_ast):
        """
        Generates an EditScript object from original and modified code
        ASTs that describes the modifications necessary to transform the
        original AST to modified AST.

        Parameters
        ----------
        first_ast : ast
            AST of original code
        second_ast : ast
            AST of modified code

        Returns
        -------
        EditScript
            Generated EditScript object that describes the modifications
            necessary to transform the original AST to modified AST
        """

        similarity_list = self.tree_differencer.connect_nodes(first_ast, second_ast)
        list_first_ast = first_ast.walk()
        list_second_ast = second_ast.walk()

        edit_script = list()

        index = 1
        while index < list_first_ast.__len__():
            node = list_first_ast[index]
            pair, similarity = self.find_node_pair(node, similarity_list)
            if not isinstance(node, (Startnode, Endnode)):
                if similarity < self.sim_treshold:
                    edit_script.append(Delete(index))
                    similarity_list = self.filter_node_pairs(node, similarity_list)
                    index += node.num_children()
                elif not node.is_mutable(pair[1]):
                    edit_script.append(Delete(index))
                    similarity_list = self.filter_node_pairs(node, similarity_list)
                    index += node.num_children()
                elif node.is_leaf() and node.similarity(pair[1]) < 1.0:
                    edit_script.append(Update(index, pair[1]))
            index += 1

        index = 1
        while index < list_second_ast.__len__():
            node = list_second_ast[index]
            pair, similarity = self.find_node_pair(node, similarity_list)
            if not isinstance(node, (Startnode, Endnode)):
                if similarity < self.sim_treshold:
                    edit_script.append(Insert(index, node))
                    index += node.num_children()
                elif not pair[0].is_mutable(pair[1]):
                    edit_script.append(Insert(index, node))
                    index += node.num_children()

            index += 1

        return EditScript(edit_script)

    def find_node_pair(self, node, similarity_list):
        pair = [key for key, value in similarity_list.items() if node in key]
        if pair:
            return pair[0], similarity_list[pair[0]]
        else:
            return None, 0

    def filter_node_pairs(self, node, similarity_list):
        return {key: value for key, value in similarity_list.items() if key[0] not in node.get_all_children()}


class TreeDifferencer:
    """
    A class that is responsible for connecting the same nodes in original and
    modified code ASTs.
    This functionality is necessary for this stage so that the EditScriptGenerator
    can create accurate EditScripts using not only insert, delete and update
    operations but also the move operation.

    ...

    Methods
    -------
    public __init__(self)
        Initialises TreeDifferencer object.
    public dict of (int, int) connect_nodes(self, original, modified)
        Generates a dictionary of AST node indexes that describes which AST nodes
        are corresponding in original and modified ASTs.

    """

    def __init__(self, f=0.1):
        """
        Initialises TreeDifferencer object.
        """
        self.f = f

    def connect_nodes(self, first_ast, second_ast):
        """
        Generates a dictionary of AST node indexes that describes which AST nodes
        are corresponding in original and modified ASTs.

        Parameters
        ----------
        first_ast : ast
            AST of original code
        second_ast : ast
            AST of modified code

        Returns
        -------
        dict of (int, int)
            Dictionary of AST node indexes that describes which AST nodes are
            corresponding in original and modified ASTs.
            The keys of the dictionary are original AST node indexes and values are
            modified AST node indexes.
        """
        in_org = first_ast.walk()
        in_mod = second_ast.walk()

        post_org = first_ast.walk(True)
        post_mod = second_ast.walk(True)

        node_pairs = self.init_leaf_pairs(post_org, post_mod, self.f)

        for i in range(1000):
            self.bottom_up(post_org, post_mod, node_pairs, self.f)
            self.top_down(in_org, in_mod, node_pairs, self.f)

        sorted_x = sorted(node_pairs.items(), key=lambda kv: kv[1], reverse=True)
        sorted_node_pairs = collections.OrderedDict(sorted_x)

        no_duplicates_node_pairs = self.remove_duplicates(sorted_node_pairs)
        
        return no_duplicates_node_pairs

    def init_leaf_pairs(self, post_order_first_ast, post_order_second_ast, f):
        leaf_pairs = dict()
        leaves_first = [x for x in post_order_first_ast if x.is_leaf()]
        leaves_second = [x for x in post_order_second_ast if x.is_leaf()]
        for x in leaves_first:
            for y in leaves_second:
                similarity = x.similarity(y)
                if similarity > f:
                    leaf_pairs[(x, y)] = similarity
        return leaf_pairs

    def bottom_up(self, post_order_first_ast, post_order_second_ast, node_pairs, f):
        inner_nodes_first = [x for x in post_order_first_ast if not x.is_leaf()]
        inner_nodes_second = [x for x in post_order_second_ast if not x.is_leaf()]
        for x in inner_nodes_first:
            for y in inner_nodes_second:
                similarity = x.similarity(y, node_pairs)
                if similarity > f:
                    node_pairs[(x, y)] = similarity

    def top_down(self, first_ast, second_ast, node_pairs, f):
        inner_nodes_first = [x for x in first_ast if not x.is_leaf()]
        inner_nodes_second = [x for x in second_ast if not x.is_leaf()]
        for x in inner_nodes_first:
            for y in inner_nodes_second:
                current_sim = self.parrent_sim_softmax(x, y,node_pairs)
                if current_sim >= 0:
                    for child_x in x.get_children(x):
                        for child_y in y.get_children(y):
                            children_sim = node_pairs.get((child_x, child_y), 0)
                            if children_sim != 0:
                                if isinstance(child_x, (Startnode, Endnode)):
                                    mean = self.arithmetic_mean(current_sim, children_sim)
                                else:
                                    mean = self.arithmetic_mean(current_sim, children_sim)
                                if mean <= f:
                                    del node_pairs[(child_x, child_y)]
                                else:
                                    node_pairs[(child_x, child_y)] = mean

    def harmonic_mean(self, x, y):
        return (2*x*y) / (x+y)

    def arithmetic_mean(self, x, y):
        return (x+y) / 2

    def parrent_sim_softmax(self, first_node, second_node, node_pairs):
        parents_sim = exp(node_pairs.get((first_node, second_node), 0))
        others_sim = sum(exp(value) for key, value in node_pairs.items() if first_node in key or second_node in key)
        if parents_sim == 1:
            return 0
        else:
            return parents_sim / others_sim

    def remove_duplicates(self, node_pairs):
        matched = list()
        no_duplicates_node_pairs = dict()
        for key, value in node_pairs.items():
            if key[0] not in matched and key[1] not in matched:
                no_duplicates_node_pairs[key] = value
                matched.append(key[0])
                matched.append(key[1])
        return no_duplicates_node_pairs

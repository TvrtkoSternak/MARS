import _ast
import ast
import collections
import copy

from similarity.sorensen_dice import SorensenDice

from mars.astutils import AstUtils
from mars.astwrapper import Startnode, Endnode
from mars.pattern import EditScript, Move, Delete, Insert, Update, Pattern


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
    def __init__(self, context, ast_parser, script_generator):
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
        self.context = context
        self.ast_parser = ast_parser
        self.script_generator = script_generator

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

        original_ast = ast.parse(text_original)
        modified_ast = ast.parse(text_modified)

        return Pattern(original_ast, modified_ast, self.script_generator.generate(original_ast, modified_ast))

    def save_pattern(self, pattern):
        """
        Saves a pattern to a database in context attribute.

        Parameters
        ----------
        created_pattern : Pattern
            Pattern that is going to be saved in the pattern database
        """
        self.context.save(pattern)


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
        self.similarity_list = None
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
        detailed_first_ast = AstUtils.walk_all_nodes(first_ast)
        detailed_second_ast = AstUtils.walk_all_nodes(second_ast)
        postorder_first_ast = []
        postorder_second_ast = []
        AstUtils.change_to_postorder(detailed_first_ast[0], postorder_first_ast)
        AstUtils.change_to_postorder(detailed_second_ast[0], postorder_second_ast)

        self.similarity_list = self.tree_differencer.connect_nodes(postorder_first_ast, postorder_second_ast)

        print("Slicnosti")
        for somethin in self.similarity_list:
            print(somethin[0].node, somethin[1].node, somethin[2], somethin[0].get_value())

        edit_script = EditScript([])

        # for node in detailed_first_ast:
        #     print(node.node, "::::", node.index, "::::", node.leaf, "::::", node.parent)

        # for node in detailed_second_ast:
        #     print(node.node, "::::", node.index, "::::", node.leaf, "::::", node.parent)

        # Original ast, here we handle the delete, update and move
        copy_sim = copy.deepcopy(self.similarity_list)
        i = 1
        num_deleted_nodes = 0
        while i < detailed_first_ast.__len__():
            node = detailed_first_ast[i]
            print("prvi prolaz: ", node)
            found_match = self.find_node_pair(node, copy_sim)
            if not found_match:
                # No match, delete node
                edit_script.add(Delete(node.index - num_deleted_nodes))
                if not node.leaf:
                    # Increment by number of children so that we don't delete them again
                    i += node.number_of_children(count_inner_nodes=True)
                    num_deleted_nodes += node.number_of_children(True) + 1
                else:
                    num_deleted_nodes += 1
            elif 1 > found_match[0][2] > self.sim_treshold:
                print('######################## ', found_match[0][0], " ", found_match[0][1])

                if node.leaf:
                    # Node is a leaf, update it
                    edit_script.add(Update(node.index - num_deleted_nodes, found_match[0][1].node))
                # else:
                #     # print('tu', node)
                #     # node is a subbtree, check if needs to move
                #     parent_match = self.find_node_pair(found_match[0][0].parent, copy_sim)
                #     if parent_match:
                #         # print('tu sam')
                #         if parent_match[0][1] is not found_match[0][1].parent:
                #             # print('tu nisam')
                #             edit_script.add(Move(node.index, found_match[0][1].index))
                    print("size: ", len(copy_sim))
                    copy_sim.remove(found_match[0])
                    print("size: ", len(copy_sim))

            i += 1

        # Modified ast, here we handle the insert
        i = 1
        while i < detailed_second_ast.__len__():
            # print(i)
            node = detailed_second_ast[i]
            found_match = self.find_node_pair(node, self.similarity_list)

            if not found_match:
                # No match, insert node
                edit_script.add(Insert(node.index, node.node))
                if not node.leaf:
                    # Increment by number of children so that we don't insert them again
                    i += node.number_of_children(count_inner_nodes=True)

            i += 1

        return edit_script

    def find_node_pair(self, node, similarity_list):
        found_match = [item for item in similarity_list if node in item]
        return found_match


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

    def __init__(self, f=0.6, t=0.6):
        """
        Initialises TreeDifferencer object.
        """
        self.f = f
        self.t = t

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

        node_pairs = self.init_leaf_pairs(post_org, post_mod, 0.1)
        # for key, value in node_pairs.items():
        #     print("LEAF MATCHES: ", key, value)

        # print("----------------------------------------")

        self.bottom_up(post_org, post_mod, node_pairs, 0.1)
        # for key, value in node_pairs.items():
        #     print("BOTTOM UP: ", key, value)

        # print("----------------------------------------")

        self.top_down(in_org, in_mod, node_pairs, 0.1)
        # for key, value in node_pairs.items():
        #     print("TOP DOWN: ", key, value)

        sorted_x = sorted(node_pairs.items(), key=lambda kv: kv[1], reverse=True)
        sorted_node_pairs = collections.OrderedDict(sorted_x)

        for key, value in sorted_node_pairs.items():
            print("-------------------------------------")
            print(key, value)
            key[0].unparse(0)
            print()
            key[1].unparse(0)
            print()
        
        return node_pairs

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

    def bottom_up(self, post_order_first_ast, post_order_second_ast, node_pairs, t):
        inner_nodes_first = [x for x in post_order_first_ast if not x.is_leaf()]
        inner_nodes_second = [x for x in post_order_second_ast if not x.is_leaf()]
        for x in inner_nodes_first:
            for y in inner_nodes_second:
                similarity = x.similarity(y, node_pairs)
                if similarity > t:
                    node_pairs[(x, y)] = similarity

    def top_down(self, first_ast, second_ast, node_pairs, f):
        inner_nodes_first = [x for x in first_ast if not x.is_leaf()]
        inner_nodes_second = [x for x in second_ast if not x.is_leaf()]
        for x in inner_nodes_first:
            for y in inner_nodes_second:
                current_sim = node_pairs.get((x, y), 0)
                if current_sim >= 0:
                    for child_x in x.get_children(x):
                        for child_y in y.get_children(y):
                            children_sim = node_pairs.get((child_x, child_y), 0)
                            if children_sim != 0:
                                if isinstance(child_x, (Startnode, Endnode)):
                                    mean = self.harmonic_mean(current_sim, children_sim)
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

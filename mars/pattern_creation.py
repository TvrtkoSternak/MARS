import ast
from similarity.sorensen_dice import SorensenDice

from mars.astutils import AstUtils, DetailedNode


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

        pass

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
        pass

    def save_pattern(self, pattern):
        """
        Saves a pattern to a database in context attribute.

        Parameters
        ----------
        created_pattern : Pattern
            Pattern that is going to be saved in the pattern database
        """
        pass


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
    def __init__(self, tree_differencer):
        """
        Initialises EditScriptGenerator object

        Parameters
        ----------
        tree_differencer : TreeDifferencer
            Object that is responsible for connecting the same nodes in
            original and modified code ASTs
        """
        self.tree_differencer = tree_differencer

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
        similarity_list = self.tree_differencer.connect_nodes(detailed_first_ast, detailed_second_ast)

        pass


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

    def __init__(self, k=2, f=0.6, t=0.6):
        """
        Initialises TreeDifferencer object.
        """
        self.f = f
        self.t = t
        self.sorensen_dice = SorensenDice(k)

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

        leaves_matches_tmp = []
        for x in first_ast:
            if x.leaf:
                # print('x ', x.node)
                for y in second_ast:
                    if y.leaf:
                        # print('y ', y.node)
                        if self.leaves_match(x, y):
                            # leaves_matches[(x, y)] = self.node_similarity(x, y)
                            leaves_matches_tmp.append((x, y, self.node_similarity(x, y)))
                            # print(x.get_value(), ' - ', y.get_value(), ' : ', self.node_similarity(x, y))
        # for leaf_pair in leaves_matches_tmp:
        #     print(leaf_pair[0].get_value(), leaf_pair[1].get_value(), leaf_pair[2])
        leaves_matches_tmp.sort(key=lambda tup: tup[2], reverse=True)
        matched = []
        leaves_matches_final = [tup for tup in leaves_matches_tmp if self.best_matches(tup, matched)]
        for leaf_pair in leaves_matches_final:
            print(leaf_pair[0].get_value(), leaf_pair[1].get_value(), leaf_pair[2])

        inner_nodes_matches = []
        for x in first_ast:
            if not x.leaf:
                for y in second_ast:
                    if not y.leaf:
                        if self.inner_nodes_match(x, y):
                            inner_nodes_matches.append((x, y, self.node_similarity(x, y)))
                        elif self.weighted_match(x, y):
                            inner_nodes_matches.append((x, y, self.node_similarity(x, y)))

    def best_matches(self, tup, matched):
        flag = (tup[0] not in matched) & (tup[1] not in matched)
        matched.append(tup[0])
        matched.append(tup[1])
        return flag

    def leaves_match(self, first_node, second_node):
        if first_node.node.__class__ is not second_node.node.__class__:
            return False
        elif self.node_similarity(first_node, second_node) < self.f:
            return False
        return True

    def inner_nodes_match(self, first_node, second_node):
        if first_node.node.__class__ is not second_node.node.__class__:
            return False
        elif (self.subtree_similarity(first_node, second_node)) < self.t:
            return False
        elif self.node_similarity(first_node, second_node) < self.f:
            return False
        return True

    def subtree_similarity(self, first_node, second_node):
        return TreeDifferencer.common_nodes(first_node, second_node)/TreeDifferencer.max_number_of_leaves(first_node, second_node)

    def weighted_match(self, first_node, second_node):
        return (self.node_similarity(first_node, second_node) < self.f)\
               & (self.subtree_similarity(first_node, second_node) >= 0.8)

    def node_similarity(self, first_node, second_node):
        return self.sorensen_dice.similarity(first_node.get_value(), second_node.get_value())

    @staticmethod
    def common_nodes(first_node, second_node):
        #to do
        return 1

    @staticmethod
    def max_number_of_leaves(first_node, second_node):
        return max(DetailedNode.number_of_leaves(first_node), DetailedNode.number_of_leaves(second_node))


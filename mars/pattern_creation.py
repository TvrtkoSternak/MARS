import ast
from similarity.sorensen_dice import SorensenDice

from mars.astutils import AstUtils
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

        edit_script = EditScript([])

        # for node in detailed_first_ast:
        #     print(node.node, "::::", node.index, "::::", node.leaf, "::::", node.parent)

        # for node in detailed_second_ast:
        #     print(node.node, "::::", node.index, "::::", node.leaf, "::::", node.parent)

        # Original ast, here we handle the delete, update and move
        i = 1
        while i < detailed_first_ast.__len__():
            node = detailed_first_ast[i]
            found_match = self.find_node_pair(node, self.similarity_list)
            if not found_match:
                # No match, delete node
                edit_script.add(Delete(node.index))
                if not node.leaf:
                    # Increment by number of children so that we don't delete them again
                    i += node.number_of_children(count_inner_nodes=True)+1
            elif 1 > found_match[0][2] > self.sim_treshold:
                if node.leaf:
                    # Node is a leaf, update it
                    edit_script.add(Update(node.index, found_match[0][1].node))
                else:
                    # print('tu', node)
                    # node is a subbtree, check if needs to move
                    parent_match = self.find_node_pair(found_match[0][0].parent, self.similarity_list)
                    if parent_match:
                        # print('tu sam')
                        if parent_match[0][1] is not found_match[0][1].parent:
                            # print('tu nisam')
                            edit_script.add(Move(node.index, found_match[0][1].index))

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

        node_pairs = []
        for x in first_ast:
            if x.leaf:
                # print('x ', x.node)
                for y in second_ast:
                    if y.leaf:
                        # print('y ', y.node)
                        if self.leaves_match(x, y):
                            # leaves_matches[(x, y)] = self.node_similarity(x, y)
                            node_pairs.append((x, y, self.node_similarity(x, y)))
                            # print(x.get_value(), ' - ', y.get_value(), ' : ', self.node_similarity(x, y))
        # for leaf_pair in leaves_matches_tmp:
        #     print(leaf_pair[0].get_value(), leaf_pair[1].get_value(), leaf_pair[2])

        for x in first_ast:
            if not x.leaf:
                for y in second_ast:
                    if not y.leaf:
                        match, similarity = self.inner_nodes_match(x, y, node_pairs)
                        if match:
                            node_pairs.append((x, y, similarity))
                        # elif self.weighted_match(x, y):
                        #     inner_nodes_matches.append((x, y, self.node_similarity(x, y)))
        # for node_pair in node_pairs:
        #     print('connect_nodesbbbbbbb:::::',node_pair[0].get_value(), node_pair[1].get_value(), node_pair[2])

        for node in first_ast[-1].children:
            self.bottom_prop_sims(node, node_pairs)

        node_pairs.sort(key=lambda tup: tup[2], reverse=True)
        matched = []
        # for node_pair in node_pairs:
        #     print('connect_nodes:::::',node_pair[0].get_value(), node_pair[1].get_value(), node_pair[2])
        node_pairs = [tup for tup in node_pairs if self.best_matches(tup, matched)]

        # print('----------------------------------------------------------------')


        for pair in node_pairs:
            if pair[0].leaf and pair[1].leaf:
                sim = self.node_similarity(pair[0], pair[1])
                node_pairs[node_pairs.index(pair)] = (pair[0], pair[1], sim)

        # for node_pair in node_pairs:
        #     print(node_pair[0].get_value(), node_pair[1].get_value(), node_pair[2])

        return node_pairs

    def best_matches(self, tup, matched):
        flag = (tup[0] not in matched) & (tup[1] not in matched)
        if flag:
            matched.append(tup[0])
            matched.append(tup[1])
        return flag

    def leaves_match(self, first_node, second_node):
        if first_node.node.__class__ is not second_node.node.__class__ or first_node.parent.node.__class__ is not second_node.parent.node.__class__:
            return False
        # elif self.node_similarity(first_node, second_node) < self.f:
        #     return False
        return True

    def inner_nodes_match(self, first_node, second_node, node_pairs):
        if first_node.node.__class__ is not second_node.node.__class__:
            return False, 0
        sim = self.subtree_similarity(first_node, second_node, node_pairs)
        if first_node.number_of_children() < 4:
            return (sim >= self.t/2), sim
        return (sim >= self.t), sim
        # elif self.node_similarity(first_node, second_node) < self.f:
        #     return False

    def subtree_similarity(self, first_node, second_node, node_pairs):
        return TreeDifferencer.common_nodes(first_node, second_node, node_pairs)/TreeDifferencer.max_number_of_leaves(first_node, second_node)

    def weighted_match(self, first_node, second_node):
        return (self.node_similarity(first_node, second_node) < self.f)\
               & (self.subtree_similarity(first_node, second_node) >= 0.8)

    def node_similarity(self, first_node, second_node):
        return self.sorensen_dice.similarity(first_node.get_value(), second_node.get_value()) / 2 + 0.5

    @staticmethod
    def common_nodes(first_node, second_node, node_pairs):
        found_pairs = []
        for first_child in first_node.children:
            for second_child in second_node.children:
                found_pairs += [(first, second, sim) for first, second, sim in node_pairs if first_child == first and second_child == second]

        averaged_similarities = 0
        for first_child in first_node.children:
            first_node_pairs = [similarity for first, _, similarity in found_pairs if first_child == first]
            if not first_node_pairs.__len__() == 0:
                averaged_similarities += sum(first_node_pairs) / first_node_pairs.__len__()

        return averaged_similarities

    def bottom_prop_sims(self, node, similarity_list):
        found_match = [item for item in similarity_list if node in item]

        for match in found_match:
            parent_match = [sim for first, second, sim in similarity_list if match[0].parent == first and match[1].parent == second]
            parent_sim = 0
            if parent_match:
                parent_sim = parent_match[0]
            index = similarity_list.index(match)
            new_match = (match[0], match[1], (parent_sim + match[2])/2)
            similarity_list[index] = new_match

        for child_node in node.children:
            self.bottom_prop_sims(child_node, similarity_list)



    @staticmethod
    def max_number_of_leaves(first_node, second_node):
        return max(first_node.number_of_direct_children(), second_node.number_of_direct_children())

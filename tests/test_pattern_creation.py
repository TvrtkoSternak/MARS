from unittest import TestCase
from unittest import main
import ast

from mars.astutils import AstUtils, DetailedNode
from mars.pattern_creation import TreeDifferencer
from mars.pattern_creation import EditScriptGenerator
from similarity.sorensen_dice import SorensenDice


class TestEditScript(TestCase):
    # def test_find_difference(self):
    #     tree_diff = TreeDifferencer(2)
    #     with open('resources/example1.py') as original:
    #         ex_one = ast.parse(original.read())
    #     with open('resources/example2.py') as original:
    #         ex_two = ast.parse(original.read())
    #
    #     tree_diff.connect_nodes(ex_one, ex_two)

    # def test_count_leaves(self):
    #     with open('resources/example1.py') as original:
    #         ex_one = ast.parse(original.read())
    #     for node in AstUtils.walk_all_nodes(ex_one):
    #         print(DetailedNode.number_of_leaves(node))

    def test_print_generated_edit_script(self):
        tree_diff = TreeDifferencer(2)
        generator = EditScriptGenerator(tree_diff, 0.5)
        with open('resources/example1.py') as original:
            ex_one = ast.parse(original.read())
        with open('resources/example2.py') as original:
            ex_two = ast.parse(original.read())
        edit_script = generator.generate(ex_one, ex_two)
        for action in edit_script:
            print(action)



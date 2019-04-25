from unittest import TestCase

from mars.pattern_creation import EditScriptGenerator, PatternCreator, TreeDifferencer
from mars.pattern_matching import Recommender, PatternFactoryListener
from mars.pattern_parsing import CounterPatternParser


class TestPatternMatching(TestCase):

    def test_number_of_matches(self):
        parser = CounterPatternParser()
        with open('resources/matching_patterns/source1.py') as source:
            source1 = source.read()
        tree_diff = TreeDifferencer(2, 0, 0)
        creator = PatternCreator(None, None, EditScriptGenerator(tree_diff, 0))
        pattern = creator.create_pattern('resources/matching_patterns/pattern1.py',
                                                'resources/matching_patterns/pattern1.py')

        recommender = Recommender(parser, source1)
        pattern_factory = PatternFactoryListener(pattern)
        pattern_factory.subscribe(recommender)

        recommender.get_recommendations()

        print(parser.get_count())
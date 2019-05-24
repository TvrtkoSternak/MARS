import ast

from mars.astutils import AstWrapper
from mars.pattern_loading import PatternFactoryLoader
from mars.pattern_matching import Recommender
from mars.pattern_parsing import ReadablePatternParser
from mars.pattern_storage import StorageContext


class Mars:
    def __init__(self):
        self.parser = ReadablePatternParser()
        self.recommender = Recommender(self.parser)

        storage_context = StorageContext()
        factories_loader = PatternFactoryLoader(storage_context)

        for listener in factories_loader.load():
            listener.subscribe(self.recommender)

    def analysis(self, code):
        nodes = AstWrapper().visit(ast.parse(code)).walk()

        self.parser.recommendation = ''
        self.recommender.get_recommendations(nodes)

        return self.parser.get_recommended_code()

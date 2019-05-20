import ast

from mars.astutils import AstWrapper
from mars.pattern_loading import PatternFactoryLoader
from mars.pattern_matching import Recommender
from mars.pattern_parsing import ReadablePatternParser
from mars.pattern_storage import StorageContext

with open("../resources/demo.py") as original:
    wrapper = AstWrapper()
    original_code = wrapper.visit(ast.parse(original.read()))
    parser = ReadablePatternParser()
    recommender = Recommender(parser)

    storageContext = StorageContext()
    factoriesLoader = PatternFactoryLoader(storageContext)

    for listener in factoriesLoader.load():
        listener.subscribe(recommender)

    list_original_code = original_code.walk()

    for index, node in enumerate(list_original_code):
        print(index, ":", node)

    recommender.get_recommendations(original_code.walk())
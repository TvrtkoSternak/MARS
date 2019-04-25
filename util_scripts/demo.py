import ast

from mars.pattern_loading import PatternFactoryLoader
from mars.pattern_matching import Recommender
from mars.pattern_parsing import XMLPatternParser
from mars.pattern_storage import filename, StorageContext

with open("C:/Users/Korisnik/Desktop/demo/demo.xml", "w+") as output, open("C:/Users/Korisnik/Desktop/demo/demo.py") as original:
    original_code = ast.parse(original.read())
    parser = XMLPatternParser(output)

    recommender = Recommender(parser, original_code)

    storageContext = StorageContext(filename)
    factoriesLoader = PatternFactoryLoader(storageContext)

    for listener in factoriesLoader.load():
        listener.subscribe(recommender)

    recommender.get_recommendations()


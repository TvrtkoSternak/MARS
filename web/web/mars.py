from mars.pattern_loading import PatternFactoryLoader
from mars.pattern_matching import Recommender
from mars.pattern_parsing import StoreRecommendationsPatternParser
from mars.pattern_storage import StorageContext, filename


class Mars:
    def __init__(self):
        self.parser = StoreRecommendationsPatternParser()
        self.recommender = Recommender(self.parser)

        storage_context = StorageContext(filename)
        factories_loader = PatternFactoryLoader(storage_context)

        for listener in factories_loader.load():
            listener.subscribe(self.recommender)

    def analysis(self, code):
        self.recommender.get_recommendations(code)

        return self.parser.recommendation

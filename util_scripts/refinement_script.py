from mars.pattern_refinement import PatternRefiner
from mars.pattern_storage import StorageContext, filename

refiner = PatternRefiner(StorageContext(filename))
refiner.refine()
from mars.pattern_creation import TreeDifferencer, EditScriptGenerator
from mars.pattern_refinement import PatternRefiner
from mars.pattern_storage import StorageContext

storage_context = StorageContext()
differencer = TreeDifferencer(0.3)
edit_script_generator = EditScriptGenerator(differencer, 0.3)
refiner = PatternRefiner(storage_context, edit_script_generator)

refiner.refine()
import os

from mars.pattern_creation import TreeDifferencer, EditScriptGenerator
from mars.pattern_refinement import PatternRefiner, FunctionPropagator, EditScriptOptimiser, WildcardUseCompressor
from mars.pattern_storage import StorageContext

os.system('python3 storage_initializing_script.py')
storage_context = StorageContext()
differencer = TreeDifferencer(0.3)
edit_script_generator = EditScriptGenerator(differencer, 0.3)
refiner = PatternRefiner(storage_context, edit_script_generator, WildcardUseCompressor(FunctionPropagator(EditScriptOptimiser())), min_no_patterns=5)

refiner.refine()

patterns = storage_context.load()

for pattern in patterns:
    print("----------------------------")
    print("original:")
    pattern.original.unparse(0)
    print("modified")
    pattern.modified.unparse(0)
    print("-----------------------------")
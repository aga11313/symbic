from regression.symbollic_trees import GenerationParameters
from regression.symbollic_trees import SymbolicTreeGenerator

gen_par = GenerationParameters(3, [1, 2, 3], ['divide', 'multiply'])

sym_tree_gen = SymbolicTreeGenerator(gen_par)
tree = sym_tree_gen.generate_random_tree_grow()
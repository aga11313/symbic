from regression.symbollic_trees import GenerationParameters, SymbolicTreeGenerator, generate_population

gen_par = GenerationParameters(5, [1, 2, 3], ['divide', 'multiply'], 3)

trees = generate_population(100, gen_par)
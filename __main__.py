from regression.symbollic_trees import GenerationParameters, SymbolicTreeGenerator, mutate_tree, crossover_trees
from testset.generate import generate_noisy_function
import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol, sin
from evaluation.evaluate import score_expression
import sys
import random
from statistics import mean
from copy import deepcopy

# symbolic regression parameters
MAX_NUMBER_OF_INDEPENDENT_VARIABLES = 1
TO_MUTATE = 50
TO_CROSSOVER = 40 # must be even
SIZE_OF_POPULATION = 100
TOP_OF_POPULATION = SIZE_OF_POPULATION - (TO_MUTATE + TO_CROSSOVER)
MAX_TREE_DEPTH = 2
TERMINALS = [1, 2, 3]
NON_TERMINALS =  ['divide', 'multiply', 'sine', 'cosine']
TOURNAMENT_SIZE = 5

# test evaluation cases constants
FUNCTION = np.cos
LOC = 0
SCALE = 0.5
NUMBER_OF_SAMPLE_POINTS = 50
UPPER_BOUNDARY = 2 * np.pi
LOWER_BOUNDARY = 0

# initialize generation params
gen_par = GenerationParameters(MAX_TREE_DEPTH, TERMINALS, NON_TERMINALS, MAX_NUMBER_OF_INDEPENDENT_VARIABLES)

# generate noisy data sample
noisy_data, x = generate_noisy_function(FUNCTION, LOC, SCALE, NUMBER_OF_SAMPLE_POINTS, UPPER_BOUNDARY, LOWER_BOUNDARY)
plt.plot(noisy_data, x, 'ro')

a = np.linspace(0,2 * np.pi,100)
# plt.plot(a, np.sin(a), 'r')

# initialize best expression variables
best_expression_score = 100000 # some arbitrary large number
best_expression = 0


# generate initial population of expressions
tree_generator = SymbolicTreeGenerator(gen_par)
current_trees_population = tree_generator.generate_population(SIZE_OF_POPULATION)

counter = 0

try:
    while True:
        print('generation {}'.format(counter))
        counter = counter + 1
        # evaluate all expressions from population
        scores = []
        for tree in current_trees_population:
            score = score_expression(x, np.reshape(noisy_data, (len(x), 1)), tree.root.expression_below, MAX_NUMBER_OF_INDEPENDENT_VARIABLES)
            scores.append(score)

        print('Mean: {}'.format(np.mean(scores)))  

        trees_and_scores = list(zip(current_trees_population, scores))
        best_tree_of_population = min(trees_and_scores, key=lambda x: x[1])[0]
        best_tree_fitness = min(trees_and_scores, key=lambda x: x[1])[1]
        best_expression = best_tree_of_population.root.expression_below
        print(best_expression, best_tree_fitness)

        # tournament
        new_population = []
        # for _ in range(SIZE_OF_POPULATION):
        while SIZE_OF_POPULATION >= len(new_population):
            tournament = [random.choice(trees_and_scores) for _ in range(TOURNAMENT_SIZE)]
            best_tree_in_tournament = min(tournament, key=lambda x: x[1])[0]
            if best_tree_in_tournament.root.size_below < 8:
                cp = deepcopy(best_tree_in_tournament)
                new_population.append(cp)

        current_trees_population = new_population

        # perform crossover and mutation
        # crossover
        for idx in range(TO_CROSSOVER//2):
            tree1 = random.choice(current_trees_population)
            tree2 = random.choice(current_trees_population)
            while tree1 == tree2:
                tree2 = random.choice(current_trees_population)
            crossover_trees(tree1, tree2)
            
        # mutation
        for idx in range(TO_MUTATE):
            tree_to_mutate = np.random.choice(current_trees_population)
            mutate_tree(tree_to_mutate, tree_generator)


except KeyboardInterrupt:
    print('Best expression: {}'.format(best_expression))
    pass


'''
Example usage of generate_noisy_function
for sin:
    x, y = generate_noisy_function(np.sin, 0, 0.1, 100, 2 * np.pi, 0)

for exponential:
    x, y = generate_noisy_function(np.square, 0, 1, 100, 10, 0)

To see the result of the noisy test sample run:
    plt.plot(x, y, 'ro')
    plt.show()

'''
plt.show()
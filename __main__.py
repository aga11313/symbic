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
from itertools import compress

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# symbolic regression parameters
MAX_NUMBER_OF_INDEPENDENT_VARIABLES = 1
TO_MUTATE = 30
TO_CROSSOVER = 50 # must be even
SIZE_OF_POPULATION = 100
TOP_OF_POPULATION = SIZE_OF_POPULATION - (TO_MUTATE + TO_CROSSOVER)
MAX_TREE_DEPTH = 4
TERMINALS = list(range(-10, 10))
NON_TERMINALS =  ['divide', 'multiply', 'add']
TOURNAMENT_SIZE = 5

# test evaluation cases constants
FUNCTION = lambda x: 7*x
LOC = 0
SCALE = 0.5
NUMBER_OF_SAMPLE_POINTS = 50
UPPER_BOUNDARY = 2 * np.pi
LOWER_BOUNDARY = 0

# read simba data from local file and extract columns accroding to the variables wanted
map_sysargs_column = {'ms': 0, 'sfr': 1, 'met': 2, 'mHI': 3, 'mH2': 4, 'mbh': 5, 'mdust': 6, 'mh': 7, 'rh': 8, 'sigh': 9}

independent = 'sfr'
dependents = ['ms']

independent_dependent = dependents + [independent]

simba_50 = np.load('simba_list_50' + '.npy')
simba_50_reshaped = simba_50.T

simba_df = pd.DataFrame(simba_50_reshaped, columns=['ms', 'sfr', 'met', 'mHI', 'mH2', 'mbh', 'mdust', 'mh', 'rh', 'sigh'])    

simba_df[independent_dependent] = simba_df[simba_df[independent_dependent] != 0][independent_dependent]
simba_df = simba_df.dropna()

simba_50_no_zeros = simba_df.to_numpy().T

simba_50_log = np.log(simba_50_no_zeros)

independent_col = simba_50_log[map_sysargs_column[independent]]
dependent_cols = simba_50_log[[map_sysargs_column[x] for x in dependents]]

# initialize generation params
gen_par = GenerationParameters(MAX_TREE_DEPTH, TERMINALS, NON_TERMINALS, MAX_NUMBER_OF_INDEPENDENT_VARIABLES)

# generate noisy data sample
noisy_data, x = generate_noisy_function(FUNCTION, LOC, SCALE, NUMBER_OF_SAMPLE_POINTS, UPPER_BOUNDARY, LOWER_BOUNDARY)
# plt.plot(noisy_data, x, 'ro')

a = np.linspace(0,2 * np.pi,100)
# plt.plot(a, np.sin(a), 'r')

plt.plot(dependent_cols[0], independent_col, 'ro')

# initialize best expression variables
best_expression_score = 100000 # some arbitrary large number
best_expression = 0


# generate initial population of expressions
tree_generator = SymbolicTreeGenerator(gen_par)
current_trees_population = tree_generator.generate_population(SIZE_OF_POPULATION)

counter = 0
best_expression = 0

try:
    while True:
        print('generation {}'.format(counter))
        counter = counter + 1
        # evaluate all expressions from population
        scores = []
        nans = []
        for idx, tree in enumerate(current_trees_population):
            score, nan_value = score_expression(independent_col, np.reshape(dependent_cols, (len(independent_col), 1)), tree.root.expression_below, MAX_NUMBER_OF_INDEPENDENT_VARIABLES)
            print('tree {}, {}, {}'.format(idx, tree.root.expression_below, score))
            scores.append(score)
            nans.append(not nan_value)

        print('Mean: {}'.format(np.mean(scores)))
        
        # mu, sigma = 200, 25
        # n, bins, patches = plt.hist(list(compress(scores, nans)))
        # plt.show()

        trees_and_scores = list(compress(zip(current_trees_population, scores, nans), nans))
        best_tree_of_population = min(trees_and_scores, key=lambda x: x[1])[0]
        best_tree_fitness = min(trees_and_scores, key=lambda x: x[1])[1]

        if best_expression_score > best_tree_fitness:
            best_expression = best_tree_of_population.root.expression_below
            best_expression_score = best_tree_fitness

        print(best_tree_of_population.root.expression_below, best_tree_fitness)

        # tournament
        new_population = []
        # for _ in range(SIZE_OF_POPULATION):
        while SIZE_OF_POPULATION >= len(new_population):
            tournament = [random.choice(trees_and_scores) for _ in range(TOURNAMENT_SIZE)]
            best_tree_in_tournament = min(tournament, key=lambda x: x[1])[0]
            best_tree_in_tournament_nan = min(tournament, key=lambda x: x[1])[2]
            if best_tree_in_tournament.root.size_below < 8 and best_tree_in_tournament_nan:
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

        print()


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
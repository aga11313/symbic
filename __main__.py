from regression.symbollic_trees import GenerationParameters, SymbolicTreeGenerator, generate_population
from testset.generate import generate_noisy_function
import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol, sin
from evaluation.evaluate import score_expression
import sys

# symbolic regression parameters
MAX_NUMBER_OF_INDEPENDENT_VARIABLES = 1
TO_MUTATE = 50
TO_CROSSOVER = 30 # must be even
SIZE_OF_POPULATION = 100
TOP_OF_POPULATION = SIZE_OF_POPULATION - (TO_MUTATE + TO_CROSSOVER)
MAX_TREE_DEPTH = 4
TERMINALS = [1, 2, 3]
NON_TERMINALS =  ['divide', 'multiply', 'sinus']

# test evaluation cases constants
FUNCTION = np.sin
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
plt.plot(a, np.sin(a), 'r')

# initialize best expression variables
best_expression_score = 100000 # some arbitrary large number
best_expression = 0

try:
    while True:
        # generate initial population of expressions
        current_trees_population = generate_population(SIZE_OF_POPULATION, gen_par)
        # evaluate all expressions from population
        scores = np.array([])
        for tree in current_trees_population:
            score = score_expression(x, np.reshape(noisy_data, (len(x), 1)), tree.expression_below, MAX_NUMBER_OF_INDEPENDENT_VARIABLES)
            scores = np.append(scores, [score])
        
        probabilites = np.divide(scores, np.sum(scores))
        sorted_score_indices = scores.argsort()

        # check if the best member of current population better than previous best
        top_of_population_score_idx = sorted_score_indices[:1][0]
        if scores[top_of_population_score_idx] < best_expression_score:
            best_expression_score = scores[top_of_population_score_idx]
            best_expression = current_trees_population[top_of_population_score_idx].expression_below

        new_trees_population = []

        for idx in range(TOP_OF_POPULATION):
            tree1 = np.random.choice(current_trees_population, probabilites)
            new_trees_population = new_trees_population + tree1

        # perform crossover and mutation
        # crossover
        for idx in range(TO_CROSSOVER/2):
            tree1 = np.random.choice(current_trees_population, p=probabilites)
            tree2 = np.random.choice(current_trees_population, p=probabilites)
            

        # mutation
        for idx in range(TO_MUTATE):
            tree_to_mutate = np.random.choice(current_trees_population)


except KeyboardInterrupt:
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
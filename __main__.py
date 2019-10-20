from regression.symbollic_trees import GenerationParameters, SymbolicTreeGenerator, generate_population
from testset.generate import generate_noisy_function
import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol, sin
from evaluation.evaluate import score_expression

# symbolic regression parameters
MAX_NUMBER_OF_INDEPENDENT_VARIABLES = 1
TOP_OF_POPULATION = 10
SIZE_OF_POPULATION = 100
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

# generate initial population of expressions
trees = generate_population(SIZE_OF_POPULATION, gen_par)

# evaluate all expressions from the initial population
scores = np.array([])
for tree in trees:
    score = score_expression(x, np.reshape(noisy_data, (len(x), 1)), tree.expression_below, MAX_NUMBER_OF_INDEPENDENT_VARIABLES)
    scores = np.append(scores, [score])

# choose the best of the population
top_of_population = scores.argsort()[:TOP_OF_POPULATION]

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
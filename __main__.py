from regression.symbollic_trees import GenerationParameters, SymbolicTreeGenerator, generate_population
from testset.generate import generate_noisy_function
import numpy as np
import matplotlib.pyplot as plt

gen_par = GenerationParameters(5, [1, 2, 3], ['divide', 'multiply'], 3)

trees = generate_population(100, gen_par)

'''
Example usage of generate_noisy_function
for sin:
    x, y = generate_noisy_function(np.square, 0, 0.1, 100, 2 * np.pi)

for exponential:
    x, y = generate_noisy_function(np.square, 0, 1, 100, 10)

To see the result of the noisy test sample run:
    plt.plot(x, y, 'ro')
    plt.show()

'''
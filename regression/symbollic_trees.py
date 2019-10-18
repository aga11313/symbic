import random
from sympy import Mul, Symbol, Integer, symbols, Pow

class SymbolicTree:
    def __init__(self):
        self.root = None

    def get_expression(self):
        # return the current tree as a mathematical expression
        pass

class Function:
    def __init__(self, type_of_function, function):
        self.type = type_of_function
        self.function = function

class NonTerminal():
    def __init__(self, name, number_of_parameters, sympy_expression):
        self.name = name
        self.number_of_parameters = number_of_parameters
        self.sympy_expression = sympy_expression

class Node:
    def __init__ (self, value, expression_below):
        self.value = value
        self.left = None
        self.right = None
        self.expression_below = expression_below

non_terminals_list = {
    'multiply': Function('non_terminal', NonTerminal('multiply', 2, Mul(Symbol('x'), Symbol('y')))),
    'divide': Function('non_terminal', NonTerminal('divide', 2, Mul(Symbol('x'), Pow(Symbol('y'), Integer(-1)))))
}

class SymbolicTreeGenerator:
    def __init__(self, generation_parameters):
        '''
        describe how the tree should be generated. Can contain params such as the maximum depth
        of the tree, expressions that can be used and what probabilites with
        '''
        self.generation_parameters = generation_parameters
        
    def generate_random_tree_grow(self):
        # return a randomly generated tree according to the passed in generation params
        return(self.grow(0))

    def grow(self, max_depth):
        if max_depth == self.generation_parameters.max_depth:
            random_terminal = random.choice(self.generation_parameters.symbolic_terminals + self.generation_parameters.numerical_terminals)
            return Node(random_terminal, random_terminal)
        else:
            random_function = random.choice(self.generation_parameters.functions)
            if random_function.type == 'numerical_terminal' or random_function.type == 'symbolic_terminal':
                return Node(random_function, random_function.function)
            else:
                if random_function.function.number_of_parameters == 2:
                    # returns the subtree for the function
                    new_tree = Node(random_function, None)
                    new_tree.right = self.grow(max_depth + 1)
                    new_tree.left = self.grow(max_depth + 1)
                    x, y = symbols('x y')
                    new_tree.expression_below = random_function.function.sympy_expression.subs(x, new_tree.left.expression_below).subs(y, new_tree.right.expression_below)
                    return  new_tree

class GenerationParameters:
    def __init__(self, max_depth, terminals, non_terminals, number_of_variables):
        self.max_depth = max_depth
        self.number_of_variables = number_of_variables

        self.numerical_terminals = list(map(lambda value: Function('numerical_terminal', value), terminals))
        self.non_terminals = list(map(lambda name: non_terminals_list[name], non_terminals))
        self.symbolic_terminals = list(map(lambda idx: Function('symbolic_terminal', Symbol('x' + str(idx))), range(number_of_variables))) 

        self.functions = self.numerical_terminals + self.symbolic_terminals + self.non_terminals


def generate_population(size, generation_parameters):
    tree_generator = SymbolicTreeGenerator(generation_parameters)
    population = []
    for _ in range(size):
        population.append(tree_generator.generate_random_tree_grow())

    return population
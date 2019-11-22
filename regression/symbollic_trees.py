import random, math
from sympy import Mul, Symbol, Integer, symbols, Pow, sin
import numpy as np

class SymbolicTree:
    def __init__(self):
        self.root = None

    def get_expression(self):
        # return the current tree as a mathematical expression
        pass

    def find_random_node(self):
        if self.root.left == None:
            leftSize = 0
        else:
            leftSize = self.root.left.size_below

        index = np.random.choice(self.root.size_below)
        if index < leftSize:
            return self.root.left.find_random_node()
        elif index == leftSize:
            return self
        else:
            return self.root.right.find_random_node()

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
    def __init__ (self, value, expression_below, size_below):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.expression_below = expression_below
        self.size_below = size_below

non_terminals_list = {
    'multiply': Function('non_terminal', NonTerminal('multiply', 2, Mul(Symbol('x'), Symbol('y')))),
    'divide': Function('non_terminal', NonTerminal('divide', 2, Mul(Symbol('x'), Pow(Symbol('y'), Integer(-1))))),
    'sinus': Function('non_terminal', NonTerminal('sinus', 1, sin(Symbol('x')))),
    'power': Function('non_terminal', NonTerminal('power', 2, Pow(Symbol('x'), Symbol('y'))))
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
        return(self.grow())

    def grow(self, current_depth=0):
        if current_depth == self.generation_parameters.max_depth:
            random_terminal = random.choice(self.generation_parameters.symbolic_terminals + self.generation_parameters.numerical_terminals)
            return Node(random_terminal, random_terminal.function, 0)
        else:
            random_function = random.choice(self.generation_parameters.functions)
            if random_function.type == 'numerical_terminal' or random_function.type == 'symbolic_terminal':
                return Node(random_function, random_function.function, 0)
            else:
                if random_function.function.number_of_parameters == 2:
                    # returns the subtree for the function
                    new_tree = Node(random_function, None, None)
                    new_tree.right = self.grow(current_depth + 1)
                    new_tree.left = self.grow(current_depth + 1)
                    new_tree.left.parent = new_tree
                    new_tree.right.parent = new_tree
                    x, y = symbols('x y')
                    new_tree.expression_below = random_function.function.sympy_expression.subs(x, new_tree.left.expression_below).subs(y, new_tree.right.expression_below)
                    new_tree.size_below = new_tree.right.size_below + new_tree.left.size_below

                elif random_function.function.number_of_parameters == 1:
                    new_tree = Node(random_function, None, None)
                    new_tree.right = None
                    new_tree.left = self.grow(current_depth + 1)
                    new_tree.left.parent = new_tree
                    x = Symbol('x')
                    new_tree.expression_below = random_function.function.sympy_expression.subs(x, new_tree.left.expression_below)
                    new_tree.size_below = new_tree.left.size_below

                return new_tree

    def generate_population(self, size):
        population = []
        for _ in range(size):
            population.append(self.generate_random_tree_grow())

        return population


class GenerationParameters:
    def __init__(self, max_depth, terminals, non_terminals, number_of_variables):
        self.max_depth = max_depth
        self.number_of_variables = number_of_variables

        self.numerical_terminals = list(map(lambda value: Function('numerical_terminal', value), terminals))
        self.non_terminals = list(map(lambda name: non_terminals_list[name], non_terminals))
        self.symbolic_terminals = list(map(lambda idx: Function('symbolic_terminal', Symbol('x' + str(idx))), range(number_of_variables))) 

        self.functions = self.numerical_terminals + self.symbolic_terminals + self.non_terminals

def mutate_tree(tree, tree_generator):
    # choose random node
    random_node = tree.find_random_node()

    new_sub_tree = tree_generator.generate_random_tree_grow()

    if random_node.parent == None:
        tree.root = new_sub_tree

    if random_node.parent.left == random_node:
        random_node.parent.left = new_sub_tree
    else:
        random_node.parent.right = new_sub_tree

    current_node = random_node.parent
    while current_node.parent != None:
        current_node.size_below = current_node.right.size_below if current_node.right else 0 + current_node.left.size_below if current_node.left else 0
        current_node = current_node.parent
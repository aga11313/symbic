import random

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
    def __init__(self, name, number_of_parameters):
        self.name = name
        self.number_of_parameters = number_of_parameters

class Node:
    def __init__ (self, value):
        self.value = value
        self.left = None
        self.right = None

non_terminals_list = {
    'multiply': Function('non_terminal', NonTerminal('multiply', 2)),
    'divide': Function('non_terminal', NonTerminal('divide', 2))
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
            return random.choice(self.generation_parameters.terminals)
        else:
            random_function = random.choice(self.generation_parameters.functions)
            if random_function.type == 'terminal':
                return random_function
            else:
                if random_function.function.number_of_parameters == 2:
                    # returns the subtree for the function
                    new_tree = Node(random_function)
                    new_tree.rigth = self.grow(max_depth + 1)
                    new_tree.left = self.grow(max_depth + 1)
                #assemble tree to return
                return  new_tree

class GenerationParameters:
    def __init__(self, max_depth, terminals, non_terminals):
        self.max_depth = max_depth

        self.terminals = list(map(lambda value: Function('terminal', value), terminals))
        self.non_terminals = list(map(lambda name: non_terminals_list[name], non_terminals))

        self.functions = self.terminals + self.non_terminals

from sympy import Symbol

def score_expression(equation_left, equation_right, expression, number_of_independent_variables):
    """
    Return the score of an expression for a certain data set. The score is simply calculated
    by taking the difference between all of the points for the expression and the data sample
        :param equation_left: An n x 1 matrix with values for the experimental (measured) data
        where n is the number of data samples
        :param equation_right: An n x m matrix with values for the experimental (measured) data
        where n is the number of data samples and m is the number of independent variables
        :param expression: the mathematical expression to be evaluated
        :param number_of_independent_variables: the total number of independent variables
    """
    expression_score = 0
    for right_data_sample_idx, right_data_sample in enumerate(equation_right):
        
        expression_value = expression
        
        # Substitute a value for all the variables in the equation
        for variable_idx in range(number_of_independent_variables):
            if not isinstance(expression_value, int):
                expression_value = expression_value.subs(Symbol('x' + str(variable_idx)), right_data_sample[variable_idx])

        # Calculate difference between value of expression and the noisy data
        if not isinstance(expression_value, int):
            expression_score = expression_score + abs((equation_left[right_data_sample_idx] - expression_value.evalf()))
        else:
            expression_score = expression_score + abs((equation_left[right_data_sample_idx] - expression_value))

    return expression_score
from sympy import Symbol, nan
import math

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
    is_result_nan = True
    for right_data_sample_idx, right_data_sample in enumerate(equation_right):
        
        expression_value = expression
        
        # Substitute a value for all the variables in the equation
        for variable_idx in range(number_of_independent_variables):
            if not isinstance(expression_value, (int, float)):
                expression_value = expression_value.subs(Symbol('x' + str(variable_idx)), right_data_sample[variable_idx])

        # Calculate difference between value of expression and the noisy data
        if not isinstance(expression_value, (int, float)):
            evaluation_result = expression_value.evalf()
            if evaluation_result != nan:
                expression_score = expression_score + ((equation_left[right_data_sample_idx] - evaluation_result)**2/len(equation_left))
                is_result_nan = False
        else:
            if not math.isnan(expression_value):
                expression_score = expression_score + ((equation_left[right_data_sample_idx] - expression_value)**2/len(equation_left))
                is_result_nan = False
                
    return math.sqrt(expression_score), is_result_nan
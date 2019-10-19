import numpy as np

def generate_noisy_function(function_as_np_expression, noise_loc, noise_scale, num_of_points, range_low, range_high):
    """
    Returns two arrays that represents a a set of noisy 2D points for a given function
        :param function_as_np_expression: Function to be made noisy
        :param noise_loc: The loc for the normal distrbution used to generate noise
        :param noise_scale: The scale for the normal distribution used to generate noise
        :param num_of_points: Number of points to sample
        :param range_low: The upper range for the function generated
        :param range_high: The lower range for the function generated
    """
    noise = np.random.normal(noise_loc, noise_scale, num_of_points)

    sample_x = np.random.random(num_of_points) * range_low - range_high
    sample_y = function_as_np_expression(sample_x)
    
    noisy_sample = sample_y + noise

    # return np.dstack((sample_x, noisy_sample))
    return sample_x, noisy_sample
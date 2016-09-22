from itertools import izip

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


def add_variables(variable_list):
    return (sum(elements) for elements in izip(*variable_list))


def show_histogram(zs, mean, std):
    fig, ax = plt.subplots(1, 1, figsize=(12, 5))

    ax.hist(list(zs), 400, normed=True)

    # plot the pdf of the normal distribution
    xs = np.linspace(mean - 4 * std, mean + 4 * std, num=100)
    ax.plot(xs, norm.pdf(xs, mean, std))

    plt.tight_layout()
    plt.show()


def create_k_uniform_variables(n, k):
    return (np.random.uniform(0.0, 1.0, n) for _ in range(k))


def create_k_normal_variables(n, k):
    return (np.random.normal(0.0, 1.0, n) for _ in range(k))


def add_uniform_variables(k):
    sample_size = 10000000 / k
    variable_list = create_k_uniform_variables(sample_size, k)
    zs = add_variables(variable_list)
    show_histogram(zs, k / 2.0, np.sqrt(k / 12.0))


def add_normal_variables(k):
    sample_size = 10000000 / k
    variable_list = create_k_normal_variables(sample_size, k)
    zs = add_variables(variable_list)
    show_histogram(zs, 0, np.sqrt(2))


if __name__ == '__main__':
    np.random.seed(1090)

    # add_uniform_variables(2)
    # add_uniform_variables(7)
    add_normal_variables(2)

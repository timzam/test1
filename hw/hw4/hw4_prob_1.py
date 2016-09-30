import matplotlib.pyplot as plt
import numpy as np


def prob_1a():
    # Load data
    data = np.loadtxt('datasets/dataset_1.txt', delimiter=',', skiprows=1)

    # Split predictors and response
    x = data[:, :-1]

    # Compute matrix of correlation coefficients
    corr_matrix = np.corrcoef(x.T)

    # Display heat map
    _, ax = plt.subplots(1, 1, figsize=(6, 6))

    ax.pcolor(corr_matrix)
    ax.set_title('Heatmap of correlation matrix')

    plt.show()


def exhaustive_search_prob_1b():
    pass


def main():
    # prob_1a()
    exhaustive_search_prob_1b()


if __name__ == '__main__':
    main()
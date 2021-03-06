import itertools
from collections import namedtuple

import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import Lasso as Lasso_Reg
from sklearn.linear_model import Ridge as Ridge_Reg

# prob 1a

Dataset_1_Data = namedtuple('Dataset_1_Data', ['x', 'y'])


def load_dataset_1():
    # Load data
    data = np.loadtxt('datasets/dataset_1.txt', delimiter=',', skiprows=1)

    # Split predictors and response
    return Dataset_1_Data(x=data[:, :-1],
                          y=data[:, -1])


def heatmap_prob_1a(dataset_1_data):
    x = dataset_1_data.x

    # Compute matrix of correlation coefficients
    corr_matrix = np.corrcoef(x.T)

    # Display heat map
    _, ax = plt.subplots(1, 1, figsize=(6, 6))

    ax.pcolor(corr_matrix)
    ax.set_title('Heatmap of correlation matrix')

    plt.show()


# prob 1b, exhaustive search

def get_regression_results(predictor_subset, x, y):
    # Use only a subset of predictors in the training data
    x_subset = x[:, predictor_subset]

    # Fit and evaluate R^2
    model = sm.OLS(y, sm.add_constant(x_subset))

    return model.fit()


def get_best_k_subset(predictor_set, size_k, x, y):
    max_r_squared = -float('inf')  # set some initial small value for max R^2 score
    best_k_subset = None  # best subset of predictors of size k
    best_results = None

    for predictor_subset in itertools.combinations(predictor_set, size_k):
        results = get_regression_results(predictor_subset, x, y)
        r_squared = results.rsquared

        # Update max R^2 and best predictor subset of size k
        # If current predictor subset has a higher R^2 score than that of the best subset
        # we've found so far, remember the current predictor subset as the best!
        if r_squared > max_r_squared:
            max_r_squared = r_squared
            best_k_subset = predictor_subset
            best_results = results

    return best_k_subset, best_results


def get_results_stats(results):
    return 'bic: %.3f, R^2: %.3f' % (results.bic, results.rsquared)


def exhaustive_search_prob_1b(dataset_1_data):
    x = dataset_1_data.x
    y = dataset_1_data.y

    # Best Subset Selection
    min_bic = float('inf')  # set some initial large value for min BIC score
    best_subset = None  # best subset of predictors
    best_results = None

    num_predictors = x.shape[1]

    # Create all possible subsets of the set of <num_predictors> predictors
    predictor_set = xrange(num_predictors)  # e.g. predictor set = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Repeat for every possible size of subset
    for size_k in xrange(1, num_predictors + 1):
        k_subset, results = get_best_k_subset(predictor_set, size_k, x, y)

        bic = results.bic

        # Update minimum BIC and best predictor subset
        # If current predictor has a lower BIC score than that of the best subset
        # we've found so far, remember the current predictor as the best!
        if bic < min_bic:
            min_bic = bic
            best_subset = k_subset
            best_results = results

        print 'k: %2d, %s, subset: %s' % (size_k, get_results_stats(results), str(k_subset))

    print 'Best subset by exhaustive search: %s, %s' % (str(best_subset), get_results_stats(best_results))


# prob 1b, step-wise forward selection

def find_best_predictor_to_add(current_predictors, remaining_predictors, x, y):
    max_r_squared = -float('inf')  # set some initial small value for max R^2
    best_predictor = None  # set some throwaway initial number for the best predictor to add
    best_results = None

    # Iterate over all remaining predictors to find best predictor to add
    for i in remaining_predictors:
        # Make copy of current set of predictors
        predictor_subset = current_predictors[:]
        # Add predictor 'i'
        predictor_subset.append(i)

        results = get_regression_results(predictor_subset, x, y)
        r_squared = results.rsquared

        # Check if we get a higher R^2 value than than current max R^2, if so, update
        if r_squared > max_r_squared:
            max_r_squared = r_squared
            best_predictor = i
            best_results = results

    return best_predictor, best_results


def stepwise_forward_selection_prob_1b(dataset_1_data):
    x = dataset_1_data.x
    y = dataset_1_data.y

    # Step-wise Forward Selection
    d = x.shape[1]  # total no. of predictors

    # Keep track of current set of chosen predictors, and the remaining set of predictors
    current_predictors = []
    remaining_predictors = range(d)

    # Set some initial large value for min BIC score for all possible subsets
    min_bic = float('inf')
    results = None

    # Keep track of the best subset of predictors
    best_subset = None

    # Iterate over all possible subset sizes, 0 predictors to d predictors
    for size in xrange(d):
        predictor, results = find_best_predictor_to_add(current_predictors, remaining_predictors, x, y)

        # Remove best predictor from remaining list, and add best predictor to current list
        remaining_predictors.remove(predictor)
        current_predictors.append(predictor)

        print 'size: %d, %s, subset: %s' % (size, get_results_stats(results), current_predictors)

        # Check if BIC for with the predictor we just added is lower than
        # the global minimum across all subset of predictors
        if results.bic < min_bic:
            best_subset = current_predictors[:]
            min_bic = results.bic
            results = results

    print 'Best step-wise forward subset selection: %s, %s' % (sorted(best_subset), get_results_stats(results))


def regression_prob_1c(dataset_1_data, regression, regression_name):
    x = dataset_1_data.x
    y = dataset_1_data.y

    reg = regression(alpha=0.01)
    reg.fit(x, y)
    coefficients = reg.coef_

    print '%s:' % regression_name
    print 'Coefficients:', coefficients
    print 'Predictors with non-zero coefficients:', [i for i, item in enumerate(coefficients) if abs(item) > 0]


def lasso_regression_prob_1c(dataset_1_data):
    regression_prob_1c(dataset_1_data, Lasso_Reg, 'Lasso')


def ridge_regression_prob_1c(dataset_1_data):
    regression_prob_1c(dataset_1_data, Ridge_Reg, 'Ridge')


def main():
    dataset_1_data = load_dataset_1()

    # heatmap_prob_1a(dataset_1_data)
    # exhaustive_search_prob_1b(dataset_1_data)
    # stepwise_forward_selection_prob_1b(dataset_1_data)
    # lasso_regression_prob_1c(dataset_1_data)
    ridge_regression_prob_1c(dataset_1_data)


if __name__ == '__main__':
    main()

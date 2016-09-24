from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd


def taxicab_density_estimation():
    nrows = 100 * 1000
    # nrows = None

    df = pd.read_csv('green_tripdata_2015-01.csv', header=0, index_col=False, usecols=['lpep_pickup_datetime'],
                     parse_dates=['lpep_pickup_datetime'], nrows=nrows)
    day_minute_list = []
    for index, row in df.iterrows():
        datetime = row[0]
        minute = datetime.minute
        hour = datetime.hour
        day_minute = minute + 60 * hour
        day_minute_list.append(day_minute)

    counter = Counter(day_minute_list)
    xs, ys = zip(*counter.items())

    _, ax = plt.subplots(1, 1, figsize=(12, 6))

    ax.plot(xs, ys)
    ax.set_xlabel('time of the day (in minutes)')
    ax.set_ylabel('number of pickups')

    plt.show()


if __name__ == '__main__':
    taxicab_density_estimation()

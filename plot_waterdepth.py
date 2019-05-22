import argparse
import csv
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import dateutil.tz
import numpy as np
import pandas as pd


def read_data(filename):
    print("Reading data from %s..." % filename)
    with open(filename, "rt") as csvfile:
        rdr = csv.reader(csvfile)
        data = []
        for row in rdr:
            data.append((row[0], row[2]))

    x, y = zip(*data)  # * operator to unpack to positional args --> unzip

    # drop the 1st elements (header names)
    x = list(x)[1:]
    y = list(y)[1:]

    return x, y


def build_graphs(data, show_graphs=False):
    """Generates graphs for data (of the form x,y). Saves files as .PNG"""
    print("Generating graphs...")
    x, y = data

    # drop the timezones (data contains a mix of values)
    # x = list(map(lambda s: s.replace(" CET", "").replace(" CEST", ""), x))

    # x = list(map(lambda d: datetime.strptime(d, "%Y-%m-%d %H:%M:%S UTC").replace(tzinfo=timezone.utc), x))
    x = list(map(
        lambda d: pd.to_datetime(str(datetime.strptime(d, "%Y-%m-%d %H:%M:%S UTC"))).replace(
            tzinfo=dateutil.tz.tzutc()),
        x))

    y = np.array(list(map(float, y)))

    # print(x)
    # print(y)

    # -----------------------------------
    # ------------- figures -------------
    # -----------------------------------

    if not show_graphs:
        matplotlib.use("Agg")  # allows figures to be generated on headless server

    # import matplotlib.pyplot as plt
    sns.set(style="darkgrid")

    # from pandas.plotting import register_matplotlib_converters
    # register_matplotlib_converters()

    # ---------- FIGURE ----------
    # plot raw data - vanilla matplotlib
    plt.plot(x, y, label="raw")

    # plot mean and std dev - using numpy
    mean = np.mean(y)
    std = np.std(y)
    plt.errorbar(x, [mean] * len(x), std, label="std dev")

    # plot rolling mean - using pandas Series
    win_size = 50
    rolling_mean = pd.Series(y).rolling(window=win_size).mean()
    plt.plot(x, rolling_mean, label="rolling (win=%d)" % win_size)

    # fig, ax = plt.subplots()#ystart, yend = ax.get_ylim()
    # plt.yticks(np.arange(0, yend, 1))
    plt.xticks(rotation='vertical')
    init_plot("Water depth readings", "date", "depth")
    plt.savefig("graphs/fig_sensor.png", bbox_inches='tight')

    # ---------- FIGURE ----------
    # avg per hour - using pandas DF
    # df = pd.DataFrame({"time": x, "depth": y})
    # avg_series = df.groupby(df["time"].dt.hour)["depth"].aggregate(np.mean)  # returns a series
    # plt.bar(avg_series.index, avg_series, label="avg / hr", width=0.6)
    # init_plot("Average water depth during the day", "hour", "depth")
    # plt.ylim(max(np.amin(avg_series) - (np.amin(avg_series) * 0.1), 0),
    #         np.amax(avg_series) + (np.amax(avg_series) * 0.1))
    # plt.savefig("graphs/fig_avg_hourly.png", bbox_inches='tight')

    # ---------- FIGURE ----------
    # drop values outside 1 std dev - using pandas DF
    # df = pd.DataFrame({"time": x, "depth": y})
    # df.set_index("time", inplace=True)
    # df = drop_1std(df)
    # df.plot()
    # init_plot("Cleaned sensor values (mean +/- 1 std)", "date", "depth")
    # ymax = df["depth"].max()
    # ymin = df["depth"].min()
    # plt.ylim(max(0, (ymin - (ymin * 0.1))), ymax + (ymax * 0.1))
    # plt.savefig("graphs/fig_clean_sensor.png", bbox_inches='tight')

    # ---------- FIGURE ----------
    # drop values outside 1 rolling std dev - using pandas DF
    df = pd.DataFrame({"time": x, "depth": y})
    df.set_index("time", inplace=True)
    df = drop_1_rolling_std(df)
    df.plot()
    init_plot("Cleaned sensor values (rolling mean +/- 1 rolling std)", "date", "depth")
    ymax = df["depth"].max()
    ymin = df["depth"].min()
    plt.ylim(max(0, (ymin - (ymin * 0.1))), ymax + (ymax * 0.1))
    plt.savefig("graphs/fig_clean_sensor.png", bbox_inches='tight')

    # ---------- FIGURE ----------
    # avg per day - using pandas DF re-indexing (and pandas plot wrapper)
    # df = pd.DataFrame({"time": x, "depth": y})
    # df.set_index("time", inplace=True)
    df = df.groupby([df.index.year, df.index.month, df.index.day]).aggregate(np.mean)
    ax = df.plot(kind="bar")  # uses plot method of df
    init_plot("Average water depth by day", "date", "depth")
    ymax = df["depth"].max()
    ymin = df["depth"].min()
    plt.ylim(max(0, (ymin - (ymin * 0.1))), ymax + (ymax * 0.1))

    # hide some xlabels (otherwise gets too busy)
    spacing = 5
    visible = ax.xaxis.get_ticklabels()[::spacing]
    for label in ax.xaxis.get_ticklabels():
        if label not in visible:
            label.set_visible(False)
    plt.savefig("graphs/fig_avg_daily.png", bbox_inches='tight')

    # show graphs?
    if show_graphs:
        plt.show()

    plt.close()


def drop_1std(df):
    mean = df.mean()["depth"]
    std = df.std()["depth"]
    return df[df["depth"].between(mean - std, mean + std)]


def drop_1_rolling_std(df):
    win_size = 50
    rolling_mean = df.rolling(window=win_size).mean()
    rolling_std = df.rolling(window=win_size).std()

    return df[
        df["depth"].between(rolling_mean["depth"] - rolling_std["depth"], rolling_mean["depth"] + rolling_std["depth"])]


def init_plot(title, xlabel, ylabel):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()


if __name__ == "__main__":
    # read command-line args
    parser = argparse.ArgumentParser(description='Analyses data from ThinkSpeak.com and generates graphs.')
    parser.add_argument('filename', help='file to process')
    parser.add_argument('--show', dest='show', action='store_true', default=False,
                        help='show graphs (as well as saving)')

    args = parser.parse_args()

    build_graphs(read_data(args.filename), args.show)

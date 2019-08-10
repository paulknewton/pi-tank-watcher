import argparse
import itertools
import math
import matplotlib
from datetime import datetime

from numpy import genfromtxt


def build_graphs(filename, show_graphs=False):
    """Generates graphs for data (of the form x,y). Saves files as .PNG"""
    print("Reading data from %s..." % filename)

    def str2date(d):
        return datetime.strptime(d.decode("utf-8"), "%Y-%m-%d %H:%M:%S UTC")

    data = genfromtxt(filename, delimiter=",", dtype=None, names=True, converters={0: str2date})
    print(data.dtype.names)

    print("Generating graphs...")

    # -----------------------------------
    # ------------- figures -------------
    # -----------------------------------

    if not show_graphs:
        matplotlib.use("Agg")  # allows figures to be generated on headless server
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(style="darkgrid")
    font = {'size': 6}
    matplotlib.rc('font', **font)

    # from pandas.plotting import register_matplotlib_converters
    # register_matplotlib_converters()

    # tuples of title/data
    graph_data = [
        ("time", data["created_at"]),
        ("temperature", data["field1"]),
        ("humidity", data["field2"]),
        ("pressure", data["field3"]),
        ("rainfall", data["field4"])
    ]

    # generate all combinations of data pairs
    # TODO does this duplicate data lists?
    pairs = list(itertools.combinations(graph_data, 2))

    # calculate grid of subplots
    subplots_cols = 3
    subplots_rows = math.ceil(len(pairs) / subplots_cols)
    print("Graph layout (%d, %d)" % (subplots_rows, subplots_cols))
    _fig, axs = plt.subplots(subplots_rows, subplots_cols, figsize=(15, 8))

    # iterate over each ax and plot the data pair
    for ax, (data_x, data_y) in zip(axs.flat, pairs):
        label_x, vector_x = data_x
        label_y, vector_y = data_y
        ax.scatter(vector_x, vector_y, c="red", s=3)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        ax.set_xlabel(label_x)
        ax.set_ylabel(label_y)

    plt.savefig("graphs/fig_weather.png", bbox_inches='tight')
    if show_graphs:
        plt.show()
    plt.close()


if __name__ == "__main__":
    # read command-line args
    parser = argparse.ArgumentParser(description='Analyses data from ThinkSpeak.com and generates graphs.')
    parser.add_argument('filename', help='file to process')
    parser.add_argument('--show', dest='show', action='store_true', default=False,
                        help='show graphs (as well as saving)')

    args = parser.parse_args()

    build_graphs(args.filename, args.show)

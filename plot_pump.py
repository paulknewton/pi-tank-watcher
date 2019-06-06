import numpy as np
import pandas as pd
import pump_watcher as pw
import csv
from numpy import genfromtxt
from datetime import datetime
import argparse
import matplotlib


def count_pump_on(data):
    # cast to int in case the data is some other type
    return len([d for d in data if int(d[1]) == pw.PUMP_ON])


def count_pump_off(data):
    # cast to int in case the data is some other type
    return len([d for d in data if int(d[1]) == pw.PUMP_OFF])


def find_next_event(data, event_type):
    for i in range(0, len(data)):
        if int(data[i][1]) == event_type:
            return data[i:]


def get_on_off_durations(data):
    data = find_next_event(data, pw.PUMP_ON)
    if not data:
        return None, None
    on_event = data[0]
    # print("next on: ", on_event)

    data = find_next_event(data[1:], pw.PUMP_OFF)
    if not data:
        return None, None
    off_event = data[0]
    # print("next off: ", off_event)

    return data, off_event[0] - on_event[0]


def get_all_durations(data):
    durations = []

    while data:
        data, pump_duration = get_on_off_durations(data)
        if pump_duration:
            pump_duration = pump_duration.total_seconds()  # convert to seconds - gives clearer graphs
            durations.append(pump_duration)

    return durations


def thingspeak_str2date(x):
    return datetime.strptime(x.decode("utf-8"), "%Y-%m-%d %H:%M:%S UTC")


def build_graphs(filename, show_graphs=False):
    """Generates graphs for pump data. Saves files as .PNG"""
    print("Reading data from %s..." % filename)

    data = genfromtxt(filename, delimiter=",", dtype=None, names=True, converters={0: thingspeak_str2date})
    print(data.dtype.names)

    print("Generating graphs...")

    if not show_graphs:
        matplotlib.use("Agg")  # allows figures to be generated on headless server
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(style="darkgrid")

    time, sample_id, event = zip(*data)  # * operator to unpack to positional args --> unzip

    # ---------- FIGURE ----------
    # plot raw data
    df = pd.DataFrame({"time": time, "pump": event})
    # print(df)
    df.plot(x="time", y="pump")
    plt.savefig("graphs/fig_pump.png", bbox_inches='tight')

    # ---------- FIGURE ----------
    # plot durations when pump is on
    durations = np.array(get_all_durations(list(zip(time, event))))
    print("durations: ", len(durations))
    print("mean duration = ", np.mean(durations))
    # print(durations)
    df = pd.DataFrame({"on duration": durations})
    # print(df)
    ax = df.plot(kind="bar")
    ax.get_xaxis().set_ticks([])    # need to clear xticks here (cannot set in .plot function)
    plt.savefig("graphs/fig_pump_durations.png", bbox_inches='tight')

    if show_graphs:
        plt.show()
    return

    std_dev = df.loc[:, "pump duration"].std()
    print("std dev = ", std_dev)

    # ---------- FIGURE ----------
    # drop 1 std dev
    mean = np.mean(durations)
    durations = durations[(durations >= mean - std_dev) & (durations <= mean + std_dev)]
    print("stripped stddev durations:", len(durations))
    print("mean duration = ", np.mean(durations))
    df = pd.DataFrame({"excl. 1 stddev pump duration": durations})
    # print(df)
    df.plot(kind="bar")

    # ---------- FIGURE ----------
    # drop upper/lower percentiles
    durations = durations[(durations >= np.percentile(durations, 10)) & (durations <= np.percentile(durations, 90))]
    print("stripped percentile durations:", len(durations))
    print("mean duration = ", np.mean(durations))
    df = pd.DataFrame({"excl. upper/lower percentile pump duration": durations})
    # print(df)
    df.plot(kind="bar")

    if show_graphs:
        plt.show()


if __name__ == "__main__":
    # read command-line args
    parser = argparse.ArgumentParser(description='Analyses data from ThinkSpeak.com and generates graphs.')
    parser.add_argument('filename', help='file to process')
    parser.add_argument('--show', dest='show', action='store_true', default=False,
                        help='show graphs (as well as saving)')
    parser.add_argument('--create', dest="create_data", action="store_true", default=False, help="create test data")
    args = parser.parse_args()

    if args.create_data:
        print("Creating test data...")
        data = pw.gen_random_samples(40)
        with open(args.filename, "w", newline='') as f:
            writer = csv.writer(f)
            header = [["created_at", "entry_id", "field1"]]
            writer.writerows(header)
            writer.writerows(data)

    build_graphs(args.filename, args.show)

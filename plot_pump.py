import numpy as np
import pandas as pd
import pump_watcher as pw
import csv
from numpy import genfromtxt
from datetime import datetime
import argparse
import matplotlib
import seaborn as sns


def count_pump_on(data):
    return len([d for d in data if d[1] == pw.PUMP_ON])


def count_pump_off(data):
    return len([d for d in data if d[1] == pw.PUMP_OFF])


def find_next_event(data, event_type):
    for i in range(0, len(data)):
        if data[i][1] == event_type:
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


def get_all_on_off_durations(data):
    durations = []

    while data:
        data, pump_duration = get_on_off_durations(data)
        if pump_duration:
            durations.append(pump_duration)

    return durations


def build_graphs(filename, show_graphs=False):
    """Generates graphs for pump data. Saves files as .PNG"""
    print("Reading data from %s..." % filename)

    str2date = lambda x: datetime.strptime(x.decode("utf-8"), "%Y-%m-%d %H:%M:%S UTC")
    data = genfromtxt(filename, delimiter=",", dtype=None, names=True, converters={0: str2date})
    print(data.dtype.names)

    print("Generating graphs...")
    sns.set(style="darkgrid")

    if not show_graphs:
        matplotlib.use("Agg")  # allows figures to be generated on headless server
    import matplotlib.pyplot as plt

    time, sample_id, event = zip(*data)  # * operator to unpack to positional args --> unzip

    # plot raw data
    df = pd.DataFrame({"time": time, "pump": event})
    #print(df)
    df.plot(x="time", y="pump")
    plt.savefig("graphs/fig_pump.png", bbox_inches='tight')

    # plot durations
    durations = np.array(get_all_on_off_durations(list(zip(time, event))))
    print("durations: ", len(durations))
    mean = np.mean(durations)
    print("mean duration = ", mean)
    df = pd.DataFrame({"pump duration": durations})
    #print(df)
    df.plot(kind="bar")
    plt.savefig("graphs/fig_pump_durations.png", bbox_inches='tight')

    std_dev = df.loc[:, "pump duration"].std()
    print("std dev = ", std_dev)

    # drop 1 std dev
    durations = durations[(durations >= mean - std_dev) & (durations <= mean + std_dev)]
    print("stripped stddev durations:", len(durations))
    print("mean duration = ", np.mean(durations))
    df = pd.DataFrame({"excl. 1 stddev pump duration": durations})
    #print(df)
    df.plot(kind="bar")

    # drop upper/lower percentiles
    durations = durations[(durations >= np.percentile(durations, 10)) & (durations <= np.percentile(durations, 90))]
    print("stripped percentile durations:", len(durations))
    print("mean duration = ", np.mean(durations))
    df = pd.DataFrame({"excl. upper/lower percentile pump duration": durations})
    #print(df)
    df.plot(kind="bar")

    plt.show()


if __name__ == "__main__":
    # read command-line args
    parser = argparse.ArgumentParser(description='Analyses data from ThinkSpeak.com and generates graphs.')
    parser.add_argument('filename', help='file to process')
    parser.add_argument('--show', dest='show', action='store_true', default=False,
                        help='show graphs (as well as saving)')
    parser.add_argument('--create', dest="create_data", action="store_true", default=False, help="create test data")
    args = parser.parse_args()

    args.create_data = True
    if args.create_data:
        print("Creating test data...")
        data = pw.gen_random_samples(40)
        with open(args.filename, "w", newline='') as f:
            writer = csv.writer(f)
            header=[["created_at", "entry_id", "field1"]]
            writer.writerows(header)
            writer.writerows(data)

    build_graphs(args.filename, args.show)

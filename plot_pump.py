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
    return len([d for d in data if int(d[2]) == pw.PUMP_ON])


def count_pump_off(data):
    # cast to int in case the data is some other type
    return len([d for d in data if int(d[2]) == pw.PUMP_OFF])


def find_next_event(data, event_type):
    for i in range(0, len(data)):
        if int(data[i][2]) == event_type:
            return data[i:]


def find_next_duration(data, event1, event2):
    """
    Get the duration of the next event1/event2 combination.

    :param data: list of tuples, of the form (datetime, int)
    :return tuple of the form (datetime, float, data) where datetime is the timestamp when event1 occurred, float is the duration between the next event1/event2 (in secs), and the remaining data with event1/event2 removed
    """
    data = find_next_event(data, event1)
    if data is None:  # could not find event
        return None, None, None
    on_event_ts = data[0][0]
    #print("next event %s @ %s" % (event1, on_event_ts))

    data = find_next_event(data[1:], event2)
    if data is None:  # could not find event
        return None, None, None
    off_event_ts = data[0][0]
    #print("next event %s @ %s" % (event2, off_event_ts))

    return on_event_ts, off_event_ts - on_event_ts, data


def create_durations_for_event_pair(data, event1, event2, col, strip_outliers=False):
    durations = []

    while data is not None:
        event_ts, pump_duration, data = find_next_duration(data, event1, event2)
        if pump_duration:
            pump_duration = pump_duration.total_seconds()  # convert to seconds - gives clearer graphs
            durations.append({'time': event_ts, col: pump_duration})

    df = pd.DataFrame(columns=["time", col])
    # df = pd.DataFrame(durations)
    if durations:  # raises exception if try to append empty list
        df = df.append(durations)

    df.set_index('time', inplace=True)

    # drop values > +/- 1 std dev
    if strip_outliers:
        mean = df.mean()
        std_dev = df.std(ddof=0)  # ddof handles single values
        df = df[
            (df >= mean - std_dev) & (df <= mean + std_dev)].dropna()  # unsure why need to explicitly drop NaN values

    return df


def thingspeak_str2date(x):
    """Convert string in ThingSpeak files to datetime"""
    return datetime.strptime(x.decode("utf-8"), "%Y-%m-%d %H:%M:%S UTC")


def build_graphs(filename, truncate, show_graphs=False):
    """Generates graphs for pump data. Saves files as .PNG"""
    print("Reading data from %s..." % filename)

    data = genfromtxt(filename, delimiter=",", dtype=None, names=True, converters={0: thingspeak_str2date})
    print("Read %d entries" % len(data))
    print(data.dtype.names)

    print("Generating graphs...")

    if not show_graphs:
        matplotlib.use("Agg")  # allows figures to be generated on headless server
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(style="dark")

    time, sample_id, event = zip(*data)  # unpack to positional args --> unzip

    # ---------- FIGURE ----------
    # plot raw data
    df = pd.DataFrame({"time": time, "pump": event})

    # truncate data
    df = df[-truncate:]
    #print("Truncating to %d entries" % truncate)
    # print(data)
    #print(df)
    df.plot(x="time", y="pump")
    plt.savefig("graphs/fig_pump.png", bbox_inches="tight")

    # ---------- FIGURE ----------
    # plot durations when pump is on/off
    # df = create_durations_df(list(zip(time, event)))
    on_off_df = create_durations_for_event_pair(data, pw.PUMP_ON, pw.PUMP_OFF, "on_duration")

    # truncate data
    on_off_df = on_off_df[-truncate:]
    #print("Truncating to %d entries" % truncate)
    #print(on_off_df)
    ax = on_off_df.plot(kind="bar", linewidth=0)
    ax.get_xaxis().set_ticks([])  # need to clear xticks here (cannot set in .plot function)
    plt.savefig("graphs/fig_pump_durations_on_off.png", bbox_inches="tight")

    off_on_df = create_durations_for_event_pair(data, pw.PUMP_OFF, pw.PUMP_ON, "off_duration")
    #off_on_df['off_duration'] = off_on_df['off_duration'].apply(lambda x: x * -1)  # plot OFF periods as -ve

    # truncate data
    off_on_df = off_on_df[-truncate:]
    #print("Truncating to %d entries" % truncate)
    # print(off_on_df)
    ax = off_on_df.plot(kind="bar", linewidth=0, logy=True)
    ax.get_xaxis().set_ticks([])  # need to clear xticks here (cannot set in .plot function)
    plt.savefig("graphs/fig_pump_durations_off_on.png", bbox_inches="tight")

    # durations_df = pd.concat([on_off_df, off_on_df], sort=False).sort_index()

    if show_graphs:
        plt.show()
    return

    # ---------- FIGURE ----------
    # drop upper/lower percentiles
    on_durations = on_durations[
        (on_durations >= np.percentile(on_durations, 10)) & (on_durations <= np.percentile(on_durations, 90))]
    print("stripped percentile durations:", len(on_durations))
    print("mean duration = ", np.mean(on_durations))
    df = pd.DataFrame({"excl. upper/lower percentile pump duration": on_durations})
    #print(df)
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

    build_graphs(args.filename, 100, args.show)

import random
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PUMP_ON = 1
PUMP_OFF = 0


def get_event(threshold):
    r = random.random()
    if r >= threshold:
        return PUMP_ON
    else:
        return PUMP_OFF


def get_mainly_on():
    return get_event(0.2)


def get_mainly_off():
    return get_event(0.8)


def gen_data(length):
    data = []

    ts = datetime.datetime.utcnow()
    for i in range(0, length):
        event = get_mainly_on()
        if (event == PUMP_ON):
            ts += datetime.timedelta(0, 45 * 60)
            ts += datetime.timedelta(0, random.randint(0, 100 * 60))
            data.append((ts, event))
            print(".")
        else:
            print("missed pump PUMP_ON")

        event = get_mainly_off()
        if (event == PUMP_OFF):
            ts = ts + datetime.timedelta(0, random.randint(0, 10 * 60))
            data.append((ts, event))
            print(".")
        else:
            print("missed pump PUMP_OFF")

    return data


def count_pump_on(data):
    return len([d for d in data if d[1] == PUMP_ON])


def count_pump_off(data):
    return len([d for d in data if d[1] == PUMP_OFF])


def find_next_event(data, event_type):
    for i in range(0, len(data)):
        if data[i][1] == event_type:
            return data[i:]


def get_on_off_durations(data):
    data = find_next_event(data, PUMP_ON)
    if not data:
        return None, None
    on_event = data[0]
    # print("next on: ", on_event)

    data = find_next_event(data[1:], PUMP_OFF)
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


if __name__ == "__main__":
    data = gen_data(50)

    # plot raw data
    x, y = zip(*data)  # * operator to unpack to positional args --> unzip
    df = pd.DataFrame({"time": x, "pump": y})
    print(df)
    df.plot(x="time", y="pump")

    # plot durations
    durations = np.array(get_all_on_off_durations(data))
    print("durations: ", len(durations))
    mean = np.mean(durations)
    print("mean duration = ", mean)
    df = pd.DataFrame({"pump duration": durations})
    print(df)
    df.plot(kind="bar")

    std_dev = df.loc[:,"pump duration"].std()
    print("std dev = ", std_dev)

    # drop upper/lower percentiles
    durations = durations[(durations >= mean - std_dev) & (durations <= mean + std_dev)]
    print("stripped stddev durations:", len(durations))
    print("mean duration = ", np.mean(durations))
    df = pd.DataFrame({"excl. 1 stddev pump duration": durations})
    print(df)
    df.plot(kind="bar")

    # drop upper/lower percentiles
    durations = durations[(durations >= np.percentile(durations, 10)) & (durations <= np.percentile(durations, 90))]
    print("stripped percentile durations:", len(durations))
    print("mean duration = ", np.mean(durations))
    df = pd.DataFrame({"excl. upper/lower percentile pump duration": durations})
    print(df)
    df.plot(kind="bar")

    plt.show()

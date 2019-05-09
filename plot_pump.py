import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pump_watcher as pw


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


if __name__ == "__main__":
    data = pw.gen_random_samples(50)
    np.savetxt("pump.csv", data, fmt=["%s", "%d", "%d"], delimiter=",", header="created_at,entry_id,field1")

    time, sample_id, event = zip(*data)  # * operator to unpack to positional args --> unzip

    # plot raw data
    df = pd.DataFrame({"time": time, "pump": event})
    print(df)
    df.plot(x="time", y="pump")
    plt.savefig("fig_pump.png", bbox_inches='tight')

    # plot durations
    durations = np.array(get_all_on_off_durations(list(zip(time, event))))
    print("durations: ", len(durations))
    mean = np.mean(durations)
    print("mean duration = ", mean)
    df = pd.DataFrame({"pump duration": durations})
    print(df)
    df.plot(kind="bar")
    plt.savefig("fig_pump_durations.png", bbox_inches='tight')

    std_dev = df.loc[:,"pump duration"].std()
    print("std dev = ", std_dev)

    # drop 1 std dev
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

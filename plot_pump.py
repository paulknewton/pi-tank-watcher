import random
import datetime
import numpy as np

ON = 1
OFF = 0


def get_event(threshold):
    r = random.random()
    if r >= threshold:
        return ON
    else:
        return OFF


def get_mainly_on():
    return get_event(0.2)


def get_mainly_off():
    return get_event(0.8)


def gen_data():
    data = []

    ts = datetime.datetime.utcnow()
    for i in range(0, 10):
        event = get_mainly_on()
        if (event == ON):
            ts += datetime.timedelta(0, 45 * 60)
            ts += datetime.timedelta(0, random.randint(0, 100 * 60))
            data.append((ts, event))
            print(".")
        else:
            print("missed pump ON")

        event = get_mainly_off()
        if (event == OFF):
            ts = ts + datetime.timedelta(0, random.randint(0, 10 * 60))
            data.append((ts, event))
            print(".")
        else:
            print("missed pump OFF")

    return data


def count_pump_on(data):
    return len([d for d in data if d[1] == ON])


def count_pump_off(data):
    return len([d for d in data if d[1] == OFF])


def find_next_event(data, event_type):
    for i in range(0, len(data)):
        if data[i][1] == event_type:
            return data[i:]


def get_on_off_durations(data):
    data = find_next_event(data, ON)
    if not data:
        return None, None
    on_event = data[0]
    # print("next on: ", on_event)

    data = find_next_event(data[1:], OFF)
    if not data:
        return None, None
    off_event = data[0]
    # print("next off: ", off_event)

    return data, np.timedelta64(off_event[0] - on_event[0])


def get_all_on_off_durations(data):
    durations = []

    while data:
        data, pump_duration = get_on_off_durations(data)
        if pump_duration:
            durations.append(pump_duration)

    return durations


if __name__ == "__main__":
    data = gen_data()
    for d in data:
        print("%s, %s" % (d[0].strftime("%y-%m-%d %H:%M:%S UTC"), d[1]))

    durations = np.array(get_all_on_off_durations(data))
    for d in durations:
        print(str(d))
    print("mean duration = ", np.mean(durations))
    #print("std dev = ", np.std(durations))

    print(np.percentile(durations, 25))
    print(np.percentile(durations, 75))
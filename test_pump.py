import plot_pump as pp
import pump_watcher as pw
import pytest
from datetime import datetime


@pytest.fixture
def setup():

    # this is the format used by ThingSpeak
    raw_data = [
        ("2019-06-06 12:12:56 UTC", "1"),
        ("2019-06-06 12:13:36 UTC", "0"),
        ("2019-06-06 12:15:22 UTC", "0"),
        ("2019-06-06 12:21:21 UTC", "0"),
        ("2019-06-06 12:42:28 UTC", "1"),
        ("2019-06-06 12:43:31 UTC", "0"),
        ("2019-06-06 13:13:41 UTC", "1"),
        ("2019-06-06 13:14:40 UTC", "0"),
        ("2019-06-06 13:20:17 UTC", "0"),
        ("2019-06-06 13:39:50 UTC", "0"),
        ("2019-06-06 13:45:49 UTC", "0"),
        ("2019-06-06 13:46:53 UTC", "0"),
        ("2019-06-06 14:19:09 UTC", "1"),
        ("2019-06-06 14:20:13 UTC", "0"),
        ("2019-06-06 14:52:28 UTC", "0"),
        ("2019-06-06 14:52:49 UTC", "0"),
        ("2019-06-06 14:53:34 UTC", "1"),
        ("2019-06-06 14:54:38 UTC", "0"),
        ("2019-06-06 14:55:08 UTC", "0"),
        ("2019-06-06 14:55:53 UTC", "0"),
        ("2019-06-06 14:57:25 UTC", "0"),
        ("2019-06-06 14:59:25 UTC", "0"),
        ("2019-06-06 15:06:28 UTC", "0"),
        ("2019-06-06 15:27:10 UTC", "0"),
        ("2019-06-06 15:27:51 UTC", "0"),
        ("2019-06-06 15:28:06 UTC", "0"),
        ("2019-06-06 15:29:08 UTC", "1"),
        ("2019-06-06 15:30:11 UTC", "0"),
        ("2019-06-06 15:32:55 UTC", "0"),
        ("2019-06-06 15:33:56 UTC", "0"),
        ("2019-06-06 15:39:59 UTC", "0"),
        ("2019-06-06 15:45:55 UTC", "0"),
        ("2019-06-06 15:52:00 UTC", "0"),
        ("2019-06-06 15:58:00 UTC", "0"),
        ("2019-06-06 16:03:55 UTC", "0"),
        ("2019-06-06 16:05:45 UTC", "1"),
        ("2019-06-06 16:06:48 UTC", "0"),
        ("2019-06-06 16:09:55 UTC", "0"),
        ("2019-06-06 16:15:55 UTC", "0"),
        ("2019-06-06 16:21:55 UTC", "0"),
        ("2019-06-06 16:27:55 UTC", "0"),
        ("2019-06-06 16:30:05 UTC", "0"),
        ("2019-06-06 16:33:55 UTC", "0"),
        ("2019-06-06 16:39:55 UTC", "0"),
        ("2019-06-06 16:43:54 UTC", "1"),
        ("2019-06-06 16:44:57 UTC", "0"),
        ("2019-06-06 16:45:56 UTC", "0"),
        ("2019-06-06 16:52:01 UTC", "0"),
        ("2019-06-06 16:55:08 UTC", "0"),
        ("2019-06-06 16:57:57 UTC", "0"),
        ("2019-06-06 17:03:57 UTC", "0"),
        ("2019-06-06 17:09:57 UTC", "0"),
        ("2019-06-06 17:15:57 UTC", "0"),
        ("2019-06-06 17:22:02 UTC", "0"),
        ("2019-06-06 17:22:53 UTC", "1"),
        ("2019-06-06 17:23:56 UTC", "0"),
        ("2019-06-06 17:28:02 UTC", "0"),
        ("2019-06-06 17:33:57 UTC", "0"),
        ("2019-06-06 17:40:02 UTC", "0"),
        ("2019-06-06 17:45:18 UTC", "0"),
        ("2019-06-06 17:52:14 UTC", "0"),
        ("2019-06-06 17:58:17 UTC", "0"),
        ("2019-06-06 18:02:41 UTC", "1"),
        ("2019-06-06 18:03:45 UTC", "0"),
        ("2019-06-06 18:43:13 UTC", "1"),
        ("2019-06-06 18:44:11 UTC", "0"),
        ("2019-06-06 19:00:22 UTC", "0"),
        ("2019-06-06 19:14:34 UTC", "0"),
        ("2019-06-06 19:20:29 UTC", "0"),
        ("2019-06-06 19:22:19 UTC", "0"),
        ("2019-06-06 19:24:49 UTC", "1"),
        ("2019-06-06 19:25:53 UTC", "0"),
        ("2019-06-06 19:28:24 UTC", "0"),
        ("2019-06-06 19:29:45 UTC", "0"),
        ("2019-06-06 19:31:44 UTC", "0"),
        ("2019-06-06 19:32:23 UTC", "0"),
        ("2019-06-06 19:34:23 UTC", "0"),
        ("2019-06-06 19:37:14 UTC", "0"),
        ("2019-06-06 19:37:30 UTC", "0"),
        ("2019-06-06 19:39:30 UTC", "0")
    ]

    str2date = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S UTC")

    # convert to datetime instances
    data = []
    for time, state in raw_data:
        data.append((str2date(time), state))
    return data


def test_count_simple():
    """Test with simple data"""
    data = [(100, 1), (101, 0), (102, 1), (103, 0)]
    assert pp.count_pump_on(data) == 2
    assert pp.count_pump_off(data) == 2


def test_count_empty():
    """Test with no data"""
    assert pp.count_pump_on([]) == 0
    assert pp.count_pump_off([]) == 0


def test_count_noisy_data(setup):
    """Test with noisy data (ON/OFF events do not appear in clean sequence"""
    data = setup
    assert pp.count_pump_on(data) == 12
    assert pp.count_pump_off(data) == 68


def test_durations_simple(setup):
    """Test when data starts cleanly with a single ON event, and ends cleanly with a singel OFF event (may include noise in between)"""
    data = setup
    assert pp.get_all_durations(data[:-8]) == [40.0, 63.0, 59.0, 64.0, 64.0, 63.0, 63.0, 63.0, 63.0, 64.0, 58.0, 64.0]


def test_durations_start_with_off(setup):
    """Test when data starts with an OFF event (instead of an ON event)"""
    data = setup
    assert pp.get_all_durations(data[1:]) == [63.0, 59.0, 64.0, 64.0, 63.0, 63.0, 63.0, 63.0, 64.0, 58.0, 64.0]


def test_durations_end_with_multiple_off(setup):
    """Test when data ends with multiple repeating OFF events"""
    data = setup
    assert pp.get_all_durations(data) == [40.0, 63.0, 59.0, 64.0, 64.0, 63.0, 63.0, 63.0, 63.0, 64.0, 58.0, 64.0]


def test_durations_missing_on():
    """Test with no ON events at all"""
    data = [(176, 0), (186, 0), (241, 0), (246, 0), (342, 0), (345, 0), (378, 0), (381, 0), (424, 0), (436, 0),
            (505, 0), (620, 0),
            (631, 0), (667, 0), (673, 0), (772, 0), (783, 0)]
    assert not pp.get_all_durations(data)


def test_data_generation():
    assert len(pw.gen_random_samples(100)) == 100


def test_callbacks():
    """Test that callbacks can be added to a pump and these are triggered by events"""
    pump = pw.SumpPump(9, test_mode=True)  # setup pump on PIN 9

    # dummy logger to record events
    class DummyLogger:
        def __init__(self):
            self.events = []

        def log(self, event):
            self.events.append(event)

    test_logger1 = DummyLogger()
    pump.add_listener(test_logger1)

    # simulate an event on PIN 9
    pump.event(9)
    assert len(test_logger1.events) == 1  # check only 1 event
    assert test_logger1.events == [
        [-1]]  # Loggers log a list of fields, even if only 1 entry. -1 is the default value if GPIO not used

    # add 2 more listeners
    test_logger2 = DummyLogger()
    pump.add_listener(test_logger2)
    test_logger3 = DummyLogger()
    pump.add_listener(test_logger3)

    # simulate an event on PIN 9
    pump.event(9)
    assert len(test_logger1.events) == 2  # check 2 events
    assert test_logger1.events == [[-1], [-1]]
    assert len(test_logger2.events) == 1
    assert test_logger2.events == [[-1]]
    assert len(test_logger3.events) == 1
    assert test_logger3.events == [[-1]]

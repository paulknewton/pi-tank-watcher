import plot_pump as pp
import pump_watcher as pw
import pytest
from datetime import datetime
import mock


@pytest.fixture
def setup():
    # this is the format used by ThingSpeak
    raw_data = [
        ("2019-06-06 12:12:56 UTC", 492, 1),
        ("2019-06-06 12:13:36 UTC", 493, 0),
        ("2019-06-06 12:15:22 UTC", 494, 0),
        ("2019-06-06 12:21:21 UTC", 495, 0),
        ("2019-06-06 12:42:28 UTC", 496, 1),
        ("2019-06-06 12:43:31 UTC", 497, 0),
        ("2019-06-06 13:13:41 UTC", 498, 1),
        ("2019-06-06 13:14:40 UTC", 499, 0),
        ("2019-06-06 13:20:17 UTC", 500, 0),
        ("2019-06-06 13:39:50 UTC", 501, 0),
        ("2019-06-06 13:45:49 UTC", 502, 0),
        ("2019-06-06 13:46:53 UTC", 503, 0),
        ("2019-06-06 14:19:09 UTC", 504, 1),
        ("2019-06-06 14:20:13 UTC", 505, 0),
        ("2019-06-06 14:52:28 UTC", 506, 0),
        ("2019-06-06 14:52:49 UTC", 507, 0),
        ("2019-06-06 14:53:34 UTC", 508, 1),
        ("2019-06-06 14:54:38 UTC", 509, 0),
        ("2019-06-06 14:55:08 UTC", 510, 0),
        ("2019-06-06 14:55:53 UTC", 511, 0),
        ("2019-06-06 14:57:25 UTC", 512, 0),
        ("2019-06-06 14:59:25 UTC", 513, 0),
        ("2019-06-06 15:06:28 UTC", 514, 0),
        ("2019-06-06 15:27:10 UTC", 515, 0),
        ("2019-06-06 15:27:51 UTC", 516, 0),
        ("2019-06-06 15:28:06 UTC", 517, 0),
        ("2019-06-06 15:29:08 UTC", 518, 1),
        ("2019-06-06 15:30:11 UTC", 519, 0),
        ("2019-06-06 15:32:55 UTC", 520, 0),
        ("2019-06-06 15:33:56 UTC", 521, 0),
        ("2019-06-06 15:39:59 UTC", 522, 0),
        ("2019-06-06 15:45:55 UTC", 523, 0),
        ("2019-06-06 15:52:00 UTC", 524, 0),
        ("2019-06-06 15:58:00 UTC", 525, 0),
        ("2019-06-06 16:03:55 UTC", 526, 0),
        ("2019-06-06 16:05:45 UTC", 527, 1),
        ("2019-06-06 16:06:48 UTC", 528, 0),
        ("2019-06-06 16:09:55 UTC", 529, 0),
        ("2019-06-06 16:15:55 UTC", 530, 0),
        ("2019-06-06 16:21:55 UTC", 531, 0),
        ("2019-06-06 16:27:55 UTC", 532, 0),
        ("2019-06-06 16:30:05 UTC", 533, 0),
        ("2019-06-06 16:33:55 UTC", 534, 0),
        ("2019-06-06 16:39:55 UTC", 535, 0),
        ("2019-06-06 16:43:54 UTC", 536, 1),
        ("2019-06-06 16:44:57 UTC", 537, 0),
        ("2019-06-06 16:45:56 UTC", 538, 0),
        ("2019-06-06 16:52:01 UTC", 539, 0),
        ("2019-06-06 16:55:08 UTC", 540, 0),
        ("2019-06-06 16:57:57 UTC", 541, 0),
        ("2019-06-06 17:03:57 UTC", 542, 0),
        ("2019-06-06 17:09:57 UTC", 543, 0),
        ("2019-06-06 17:15:57 UTC", 544, 0),
        ("2019-06-06 17:22:02 UTC", 545, 0),
        ("2019-06-06 17:22:53 UTC", 546, 1),
        ("2019-06-06 17:23:56 UTC", 547, 0),
        ("2019-06-06 17:28:02 UTC", 548, 0),
        ("2019-06-06 17:33:57 UTC", 549, 0),
        ("2019-06-06 17:40:02 UTC", 550, 0),
        ("2019-06-06 17:45:18 UTC", 551, 0),
        ("2019-06-06 17:52:14 UTC", 552, 0),
        ("2019-06-06 17:58:17 UTC", 553, 0),
        ("2019-06-06 18:02:41 UTC", 554, 1),
        ("2019-06-06 18:03:45 UTC", 555, 0),
        ("2019-06-06 18:43:13 UTC", 556, 1),
        ("2019-06-06 18:44:11 UTC", 557, 0),
        ("2019-06-06 19:00:22 UTC", 558, 0),
        ("2019-06-06 19:14:34 UTC", 559, 0),
        ("2019-06-06 19:20:29 UTC", 560, 0),
        ("2019-06-06 19:22:19 UTC", 561, 0),
        ("2019-06-06 19:24:49 UTC", 562, 1),
        ("2019-06-06 19:25:53 UTC", 563, 0),
        ("2019-06-06 19:28:24 UTC", 564, 0),
        ("2019-06-06 19:29:45 UTC", 565, 0),
        ("2019-06-06 19:31:44 UTC", 566, 0),
        ("2019-06-06 19:32:23 UTC", 567, 0),
        ("2019-06-06 19:34:23 UTC", 568, 0),
        ("2019-06-06 19:37:14 UTC", 569, 0),
        ("2019-06-06 19:37:30 UTC", 570, 0),
        ("2019-06-06 19:39:30 UTC", 571, 0)
    ]

    str2date = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S UTC")

    # convert to datetime instances
    data = []
    for time, entry_id, state in raw_data:
        data.append((str2date(time), entry_id, state))
    return data


def test_count_simple():
    """Test with simple data"""
    data = [(100, 10, 1), (101, 11, 0), (102, 12, 1), (103, 13, 0)]
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
    """Test when data starts cleanly with a single ON event, and ends cleanly with a single OFF event (may include noise in between)"""
    data = setup
    test = pp.create_durations_for_event_pair(data[:-8], pw.PUMP_ON, pw.PUMP_OFF, "values")["values"].tolist()
    target = [40.0, 63.0, 59.0, 64.0, 64.0, 63.0, 63.0, 63.0, 63.0, 64.0, 58.0, 64.0]
    assert test == target


def test_durations_with_strings(setup):
    """Test when on/off events are stored as strings"""
    data = setup
    events_as_strings = [(time, str(event_id), str(event)) for time, event_id, event in data]
    test = pp.create_durations_for_event_pair(data[:-8], pw.PUMP_ON, pw.PUMP_OFF, "values")["values"].tolist()
    target = [40.0, 63.0, 59.0, 64.0, 64.0, 63.0, 63.0, 63.0, 63.0, 64.0, 58.0, 64.0]
    assert test == target


def test_durations_start_with_off(setup):
    """Test when data starts with an OFF event (instead of an ON event)"""
    data = setup
    test = pp.create_durations_for_event_pair(data[1:], pw.PUMP_ON, pw.PUMP_OFF, "values")["values"].tolist()
    target = [63.0, 59.0, 64.0, 64.0, 63.0, 63.0, 63.0, 63.0, 64.0, 58.0, 64.0]
    assert test == target


def test_durations_end_with_multiple_off(setup):
    """Test when data ends with multiple repeating OFF events"""
    data = setup
    test = pp.create_durations_for_event_pair(data, pw.PUMP_ON, pw.PUMP_OFF, "values")["values"].tolist()
    target = [40.0, 63.0, 59.0, 64.0, 64.0, 63.0, 63.0, 63.0, 63.0, 64.0, 58.0, 64.0]
    assert test == target


def test_durations_missing_on(setup):
    """Test with no ON events at all"""
    data = setup
    data2 = data[-9:]
    test = pp.create_durations_for_event_pair(data2, pw.PUMP_ON, pw.PUMP_OFF, "test_on_duration")
    print(test)


#    assert test.empty


def test_data_generation():
    assert len(pw.gen_random_samples(100)) == 100


@mock.patch("pump_watcher.SumpPump.get_status")
def test_callbacks(mock_get_status):
    """Test that callbacks can be added to a pump and these are triggered by events"""
    pump = pw.AbstractPump(9)  # setup pump on PIN 9
    mock_get_status.side_effect = [1, 0, 0]  # event order is important (X, Y, Y)

    # dummy logger to record events
    class DummyLogger:
        def __init__(self):
            self.events = []

        def log(self, event):
            self.events.append(event)

    test_logger1 = DummyLogger()
    pump.add_listener(test_logger1)

    # simulate an event
    pump.event()
    assert len(test_logger1.events) == 1  # check only 1 event
    assert test_logger1.events == [
        [1]]  # Loggers log a list of fields, even if only 1 entry. -1 is the default value if GPIO not used

    # add 2 more listeners
    test_logger2 = DummyLogger()
    pump.add_listener(test_logger2)
    test_logger3 = DummyLogger()
    pump.add_listener(test_logger3)

    # simulate a (different) event
    pump.event()
    assert len(test_logger1.events) == 2  # check 2 events
    assert test_logger1.events == [[1], [0]]
    assert len(test_logger2.events) == 1
    assert test_logger2.events == [[0]]
    assert len(test_logger3.events) == 1
    assert test_logger3.events == [[0]]

    # simulate the same event (should skip)
    pump.event()
    assert len(test_logger1.events) == 2  # check 2 events
    assert test_logger1.events == [[1], [0]]
    assert len(test_logger2.events) == 1
    assert test_logger2.events == [[0]]
    assert len(test_logger3.events) == 1
    assert test_logger3.events == [[0]]

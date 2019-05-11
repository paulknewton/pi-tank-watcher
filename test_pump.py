import plot_pump as pp
import pump_watcher as pw
import pytest


@pytest.fixture
def setup():
    data = [(176, 1), (186, 0), (241, 1), (246, 0), (342, 1), (345, 0), (378, 1), (381, 0), (424, 1), (436, 0),
            (505, 1), (620, 1),
            (631, 0), (667, 1), (673, 0), (772, 1), (783, 0)]
    return data


def test_count_simple():
    data = [(100, 1), (101, 0), (102, 1), (103, 0)]
    assert pp.count_pump_on(data) == 2
    assert pp.count_pump_off(data) == 2


def test_count_empty():
    assert pp.count_pump_on([]) == 0
    assert pp.count_pump_off([]) == 0


def test_count_missing(setup):
    data = setup
    assert pp.count_pump_on(data) == 9
    assert pp.count_pump_off(data) == 8


def test_durations(setup):
    data = setup
    assert pp.get_all_on_off_durations(data) == [10, 5, 3, 3, 12, 126, 6, 11]


def test_durations_trailing(setup):
    data = setup
    data.append((data[-1][0] + 1, 1))
    assert pp.get_all_on_off_durations(data) == [10, 5, 3, 3, 12, 126, 6, 11]


def test_durations_missing_on():
    data = [(176, 0), (186, 0), (241, 0), (246, 0), (342, 0), (345, 0), (378, 0), (381, 0), (424, 0), (436, 0),
            (505, 0), (620, 0),
            (631, 0), (667, 0), (673, 0), (772, 0), (783, 0)]
    assert not pp.get_all_on_off_durations(data)


def test_data_generation():
    assert len(pw.gen_random_samples(100)) == 100


def test_callbacks():
    pump = pw.SumpPump(9, test_mode=True)   # setup pump on PIN 9

    # dummy logger to record events
    class DummyLogger:
        def __init__(self):
            self.events = []

        def log(self, event):
            self.events.append(event)

    test_logger = DummyLogger()
    pump.add_listener(test_logger)

    # simulate an event on PIN 9
    pump.event(9)

    assert len(test_logger.events) == 1     # check only 1 event
    assert test_logger.events[0] == [-1]    # Loggers log a list of fields, even if only 1 entry. -1 is the default value if GPIO not used
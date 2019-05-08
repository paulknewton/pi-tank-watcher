import plot_pump as pp
import pytest


@pytest.fixture
def setup():
    data = [(176, 1), (186, 0), (241, 1), (246, 0), (342, 1), (345, 0), (378, 1), (381, 0), (424, 1), (436, 0), (505, 1), (620, 1),
 (631, 0), (667, 1), (673, 0), (772, 1), (783, 0)]
    return data


def test_count_on(setup):
    data = setup
    assert pp.count_pump_on(data) == 9


def test_count_off(setup):
    data = setup
    assert pp.count_pump_off(data) == 8


def test_durations(setup):
    data = setup
    assert pp.get_all_on_off_durations(data) == [10, 5, 3, 3, 12, 126, 6, 11]

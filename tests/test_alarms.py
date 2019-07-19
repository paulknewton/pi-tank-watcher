from mock import Mock
import loggers
from functools import partial
import alarm


def test_is_event_logged():
    is_10_logged = partial(alarm.is_event_logged, 10)

    alarm_clock = loggers.AlarmClock()
    print_alarm = Mock()
    alarm_clock.add_alarm(is_10_logged, print_alarm)

    # check alarm is called/not called for various events

    alarm_clock.log(8)
    assert not print_alarm.called

    alarm_clock.log(9)
    assert not print_alarm.called

    alarm_clock.log(10)
    assert print_alarm.called


def test_is_event_greater():
    f = partial(alarm.is_last_event_greater, 10)

    alarm_clock = loggers.AlarmClock()
    print_alarm = Mock()
    alarm_clock.add_alarm(f, print_alarm)

    alarm_clock.log(9)
    assert not print_alarm.called

    alarm_clock.log(10)
    assert not print_alarm.called

    alarm_clock.log(11)
    alarm_clock.log(12)
    assert print_alarm.call_count == 2


def test_is_event_less():
    f = partial(alarm.is_last_event_less, 10)

    alarm_clock = loggers.AlarmClock()
    print_alarm = Mock()
    alarm_clock.add_alarm(f, print_alarm)

    alarm_clock.log(11)
    assert not print_alarm.called

    alarm_clock.log(10)
    assert not print_alarm.called

    alarm_clock.log(9)
    alarm_clock.log(8)
    alarm_clock.log(7)
    assert print_alarm.call_count == 3

def is_event_logged(event, events):
    """
    Check if an event was logged in events

    :param event: the event to check
    :param events: the list of events already logged
    :return: true if the event has been logged, otherwise false
    """
    return event in events


def is_last_event_greater(gt, events):
    """
    Check if the last event was greater than a specified value

    :param gt: the threshold to return true
    :param events: the list of events already logged
    :return: true if the last event was greater than gt, otherwise false
    """
    return events[-1] > gt


def is_last_event_less(lt, events):
    """
    Check if the last event was less than a specified value

    :param lt: the threshold to return true
    :param events: the list of events already logged
    :return: true if the last event was less than lt, otherwise false
    """
    return events[-1] < lt

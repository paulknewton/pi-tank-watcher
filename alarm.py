def is_event_logged(event, events):
    return event in events


def is_last_event_greater(gt, events):
    return events[-1] > gt


def is_last_event_less(lt, events):
    return events[-1] < lt

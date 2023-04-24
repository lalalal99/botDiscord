from datetime import datetime

import pytz


def setToFalse(object, attrs):
    # attrs = set(object.__dict__.keys())
    # attrs = attrs.intersection(list)
    for attr in attrs:
        if hasattr(object, attr):
            setattr(object, attr, False)
        else:
            raise AttributeError(f'{attr} not in object attributes')


def getHoursMinutes():
    return datetime.now(pytz.timezone("Europe/Rome")).strftime("%H:%M")


def capitalize(word):
    return word[0].upper() + word[1:]

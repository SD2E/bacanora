import os
import datetime
import re

__all__ = [
    'current_time', 'normpath', 'normalize', 'microseconds', 'nanoseconds'
]


def current_time():
    """Current UTC time
    Returns:
        A ``datetime`` object rounded to millisecond precision
    """
    return datetime.datetime.fromtimestamp(
        int(datetime.datetime.utcnow().timestamp() * 1000) / 1000)


def microseconds():
    """Current time in microseconds as ``int``
    """
    return int(round(datetime.datetime.utcnow().timestamp() * 1000 * 1000))


def nanoseconds():
    return int(
        round(datetime.datetime.utcnow().timestamp() * 1000 * 1000 * 1000))


def normalize(filepath):
    """Trim leading slash or slashes from a path
    """
    fp = re.sub('^(/)+', '', filepath)
    return fp


def normpath(filepath):
    """Collapse duplicate leading slashes and resolve relative references
    in a path
    """
    fp = re.sub('^(/)+', '/', filepath)
    if not filepath.startswith('/'):
        filepath = '/' + filepath
    return os.path.normpath(fp)

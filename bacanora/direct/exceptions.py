"""Tapis processor failures and errors
"""


class DirectOperationFailed(OSError):
    """An error has prevented the POSIX action from being completed
    """
    pass


class UnknowableOutcome(Exception):
    """The outcome might be False but it is possible the POSIX action
    simply cannot be performed on the host
    """
    pass

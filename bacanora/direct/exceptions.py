"""Direct processor failures and errors
"""


class DirectOperationFailed(Exception):
    """An error has prevented the POSIX action from being completed
    """
    pass


class UnknowableOutcome(DirectOperationFailed):
    """The outcome might be False but it is possible the POSIX action
    simply cannot be performed on the host
    """
    pass

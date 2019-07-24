"""Tapis processor failures and errors
"""
from agavepy.agave import AgaveError
from requests.exceptions import HTTPError

__all__ = [
    'TapisOperationFailed', 'HTTPNotFoundError', 'ImportNotCompleteError'
]


class TapisOperationFailed(AgaveError):
    pass


class HTTPNotFoundError(HTTPError):
    pass


class ImportNotCompleteError(HTTPNotFoundError):
    pass

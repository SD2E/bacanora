from agavepy.agave import AgaveError
from requests.exceptions import HTTPError

__all__ = ['TapisOperationFailed', 'AgaveError', 'HTTPError']


class TapisOperationFailed(AgaveError):
    pass

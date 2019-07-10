"""Top-level exceptions and errors
"""
from agavepy.agave import AgaveError
from requests.exceptions import HTTPError

__all__ = ['AgaveError', 'HTTPError']

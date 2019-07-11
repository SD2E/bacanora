"""S3 processor failures and errors
"""
from ..direct import (DirectOperationFailed, UnknowableOutcome)
from ..stores import UnknownStorageSystem

__all__ = ['S3OperationFailed', 'S3NotSupported']


class S3OperationFailed(DirectOperationFailed):
    """An S3-to-Tapis files operation did not succeed
    """
    pass


class S3NotSupported(UnknownStorageSystem):
    """There is no S3 upload support for the storageSystem
    """
    pass

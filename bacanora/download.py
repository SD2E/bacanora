"""Facades for Tapis ``files-get`` operations
"""
from . import logger as loggermodule
from . import settings
from .processors import process, ProcessingOperationFailed

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['get']


def get(file_path,
        system_id=DEFAULT_SYSTEM_ID,
        local_filename=None,
        force=False,
        atomic=True,
        permissive=False,
        agave=None):
    """Download a file from a Tapis storageSystem

    Args:
        file_path (str): Path on the storageSystem to download
        system_id (str, optional): Tapis storageSystem to act upon
        local_filename (str, optional): Local name of downloaded file
        force (bool, optional): Force overwrite of an existing file or directory
        atomic (bool, optional): Whether to download first to a temporary file
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        str: Name of the downloaded file

    Raises:
        ProcessingOperationFailed: Some error prevented the action from completing
    """
    return process(
        'get',
        file_path=file_path,
        system_id=system_id,
        local_filename=local_filename,
        force=force,
        atomic=atomic,
        permissive=permissive,
        agave=agave)

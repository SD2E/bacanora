"""Facades for the Tapis ``stat`` operations
"""
from . import logger as loggermodule
from . import settings
from .processors import process

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['exists', 'isfile', 'isdir']


def exists(file_path,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           permissive=False,
           agave=None):
    """Determine if a path exists on a Tapis storageSystem

    Emulates Python ``os.path.exists()``

    Arguments:
        file_path (str): The path from which to fetch attributes
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path exists and False if not

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
    """
    return process(
        'exists',
        file_path=file_path,
        system_id=system_id,
        root_dir=root_dir,
        permissive=permissive,
        agave=agave)


def isfile(file_path,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           permissive=False,
           agave=None):
    """Determine if a path exists and is a file on a Tapis storageSystem

    Emulates Python ``os.path.isfile()``

    Arguments:
        file_path (str): The path from which to fetch attributes
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path is a file and False if not

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
    """
    return process(
        'isfile',
        file_path=file_path,
        system_id=system_id,
        root_dir=root_dir,
        permissive=permissive,
        agave=agave)


def isdir(dir_path,
          system_id=DEFAULT_SYSTEM_ID,
          root_dir='/',
          permissive=False,
          agave=None):
    """Determine if a path exists and is a directory on a Tapis storageSystem

    Emulates Python ``os.path.isdir()``

    Arguments:
        file_path (str): The path from which to fetch attributes
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path is a directory and False if not

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
    """
    return process(
        'isdir',
        file_path=dir_path,
        system_id=system_id,
        root_dir=root_dir,
        permissive=permissive,
        agave=agave)
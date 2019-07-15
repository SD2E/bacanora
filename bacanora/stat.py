"""Facades for the Tapis ``files-list`` operations
"""
from deprecated.sphinx import deprecated, versionadded
from . import logger as loggermodule
from . import settings
from .processors import process

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['exists', 'isfile', 'isdir']


@versionadded(version='1.0.0', reason="First release")
def exists(file_path,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           runtime=None,
           permissive=False,
           agave=None):
    """Determine if a path exists on a Tapis storageSystem

    Emulates Python ``os.path.exists()``

    Args:
        file_path (str): The path from which to fetch attributes
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        runtime (string, optional): Override detected Bacanora runtime
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
        runtime=runtime,
        root_dir=root_dir,
        permissive=permissive,
        agave=agave)


@versionadded(version='1.0.0', reason="First release")
def isfile(file_path,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           runtime=None,
           permissive=False,
           agave=None):
    """Determine if a path exists and is a file on a Tapis storageSystem

    Emulates Python ``os.path.isfile()``

    Args:
        file_path (str): The path from which to fetch attributes
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        runtime (string, optional): Override detected Bacanora runtime
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
        runtime=runtime,
        permissive=permissive,
        agave=agave)


@versionadded(version='1.0.0', reason="First release")
def isdir(dir_path,
          system_id=DEFAULT_SYSTEM_ID,
          root_dir='/',
          runtime=None,
          permissive=False,
          agave=None):
    """Determine if a path exists and is a directory on a Tapis storageSystem

    Emulates Python ``os.path.isdir()``

    Args:
        file_path (str): The path from which to fetch attributes
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        runtime (string, optional): Override detected Bacanora runtime
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
        runtime=runtime,
        permissive=permissive,
        agave=agave)

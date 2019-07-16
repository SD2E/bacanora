"""Provides ``files-list`` operations
"""
import os
import shutil
from ..utils import nanoseconds, microseconds, normalize, normpath
from .. import logger as loggermodule
from .. import settings
from .utils import abs_path
from ..stores import ManagedStoreError
from .exceptions import DirectOperationFailed, UnknowableOutcome

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['exists', 'isfile', 'isdir', 'islink', 'ismount']


def exists(file_path,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           runtime=None,
           permissive=False,
           agave=None):
    """Emulate Tapis files-list to check if a path exists on a storageSystem

    Arguments:
        file_path (str): The path to check
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        runtime (str, optional): Override the detected Bacanora runtime
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path exists and False if not

    Raises:
        UnknowableOutcome: Path was not conclusively absent
        DirectOperationFailed: Some other error prevented the operation
    """
    try:
        posix_path = abs_path(
            file_path,
            system_id=system_id,
            root_dir=root_dir,
            runtime=runtime,
            agave=agave)
        logger.info('exists({})'.format(posix_path))
        if os.path.exists(posix_path):
            logger.debug('exists({}): True'.format(posix_path))
            return True
        else:
            logger.warning('exists({}): ???'.format(posix_path))
            raise UnknowableOutcome()
    except UnknowableOutcome:
        raise
    except Exception as exc:
        raise DirectOperationFailed('Unable to complete os.path.exists()', exc)


def isfile(file_path,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           runtime=None,
           permissive=False,
           agave=None):
    """Emulate Tapis files-list to learn if file_path is a file on a storageSystem

    Arguments:
        file_path (str): The path to check
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        runtime (str, optional): Override the detected Bacanora runtime
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path is a file and False if not

    Raises:
        UnknowableOutcome: Path was not conclusively absent
        DirectOperationFailed: Some other error prevented the operation
    """
    try:
        posix_path = abs_path(
            file_path,
            system_id=system_id,
            root_dir=root_dir,
            runtime=runtime,
            agave=agave)
        logger.info('isfile({})'.format(posix_path))
        if os.path.isfile(posix_path):
            logger.debug('isfile({}): True'.format(posix_path))
            return True
        else:
            logger.warning('isfile({}): ???'.format(posix_path))
            raise UnknowableOutcome()
    except UnknowableOutcome:
        raise
    except Exception as exc:
        raise DirectOperationFailed('Unable to complete os.path.isfile()', exc)


def isdir(file_path,
          system_id=DEFAULT_SYSTEM_ID,
          root_dir='/',
          runtime=None,
          permissive=False,
          agave=None):
    """Emulate Tapis files-list to learn if file_path is a directory on a storageSystem

    Arguments:
        file_path (str): The path to check
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        runtime (str, optional): Override the detected Bacanora runtime
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path is a directory and False if not

    Raises:
        UnknowableOutcome: Path was not conclusively absent
        DirectOperationFailed: Some other error prevented the operation
    """
    posix_path = abs_path(
        file_path,
        system_id=system_id,
        root_dir=root_dir,
        runtime=runtime,
        agave=agave)
    logger.info('isdir({})'.format(posix_path))
    try:
        if os.path.isdir(posix_path):
            logger.debug('isdir({}): True'.format(posix_path))
            return True
        else:
            logger.warning('isdir({}): ???'.format(posix_path))
            raise UnknowableOutcome()
    except UnknowableOutcome:
        raise
    except Exception:
        raise DirectOperationFailed('Unable to complete os.path.isdir()')


def islink(file_path,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           runtime=None,
           permissive=False,
           agave=None):
    posix_path = abs_path(
        file_path,
        system_id=system_id,
        root_dir=root_dir,
        runtime=runtime,
        agave=agave)
    """Extend Tapis files-list to learn if file_path is a link on a storageSystem

    Arguments:
        file_path (str): The path to check
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        runtime (str, optional): Override the detected Bacanora runtime
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path is a link and False if not

    Raises:
        UnknowableOutcome: Path was not conclusively absent
        DirectOperationFailed: Some other error prevented the operation
    """
    try:
        if os.path.islink(posix_path):
            return True
        else:
            raise UnknowableOutcome()
    except UnknowableOutcome:
        raise
    except Exception:
        raise DirectOperationFailed('Unable to complete os.path.islink()')


def ismount(file_path,
            system_id=DEFAULT_SYSTEM_ID,
            root_dir='/',
            runtime=None,
            permissive=False,
            agave=None):
    """Extend Tapis files-list to learn if file_path is a mount on a storageSystem

    Arguments:
        file_path (str): The path to check
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        runtime (str, optional): Override the detected Bacanora runtime
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path is a mount and False if not

    Raises:
        UnknowableOutcome: Path was not conclusively absent
        DirectOperationFailed: Some other error prevented the operation
    """
    posix_path = abs_path(
        file_path,
        system_id=system_id,
        root_dir=root_dir,
        runtime=runtime,
        agave=agave)
    try:
        if os.path.ismount(posix_path):
            return True
        else:
            raise UnknowableOutcome()
    except UnknowableOutcome:
        raise
    except Exception:
        raise DirectOperationFailed('Unable to complete os.path.ismount()')

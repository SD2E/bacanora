"""POSIX implementations of Tapis ``files-[manage]`` operations
"""
import os
import shutil
from ..utils import nanoseconds, microseconds, normalize, normpath
from .. import logger as loggermodule
from .. import settings
from .stat import exists, isdir, isfile
from .utils import abs_path
from ..stores import ManagedStoreError
from .exceptions import DirectOperationFailed

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['mkdir', 'delete', 'rename', 'move', 'copy']


def mkdir(path_to_make,
          system_id=DEFAULT_SYSTEM_ID,
          root_dir='/',
          runtime=None,
          force=False,
          permissive=False,
          agave=None):
    """Emulate Tapis files-mkdir via makedirs() on the local host

    Args:
        path_to_make (str): Path on the storageSystem to make
        system_id (str, optional): Tapis storageSystem to act upon
        root_dir (str, optional): Base directory if path_to_delete is relative
        runtime (str, optional): Override the detected Bacanora runtime
        force (bool, optional): Force overwrite of an existing file or directory
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        bool: True on success, False on failure if permissive=True

    Raises:
        HTTPError: Underlying transport or web service error was encountered
        DirectOperationFailed: Some other error was encountered
    """
    try:
        posix_path = abs_path(
            path_to_make,
            system_id=system_id,
            root_dir=root_dir,
            runtime=runtime,
            agave=agave)
        logger.debug('mkdir: {}'.format(posix_path))
        if os.path.exists(posix_path):
            if force:
                delete(
                    path_to_make,
                    system_id=system_id,
                    root_dir=root_dir,
                    runtime=runtime,
                    agave=agave)
            else:
                raise DirectOperationFailed(
                    'Destination {} exists. Repeat with force=True to overwrite.'
                    .format(path_to_make))
        os.makedirs(posix_path, exist_ok=True)
        return True
    except Exception as err:
        if permissive:
            return False
        else:
            raise DirectOperationFailed(
                'Exception encountered with os.makedirs()', err)


def delete(path_to_delete,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           force=False,
           runtime=None,
           recursive=True,
           permissive=False,
           agave=None):
    """Emulate Tapis files-delete via remove() or rmtree() on the local host

    Args:
        path_to_delete (str): Path on the storageSystem to delete
        system_id (str, optional): Tapis storageSystem to act upon
        root_dir (str, optional): Base directory if path_to_delete is relative
        runtime (str, optional): Override the detected Bacanora runtime
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        bool: True on success, False on failure if permissive=True

    Raises:
        HTTPError: Underlying transport or web service error was encountered
        DirectOperationFailed: Some other error was encountered
    """
    try:
        posix_path = abs_path(
            path_to_delete,
            system_id=system_id,
            root_dir=root_dir,
            runtime=runtime,
            agave=agave)
        logger.debug('delete: {}'.format(posix_path))
        if not os.path.exists(posix_path):
            logger.warning('{} does not exist')
        if os.path.isfile(posix_path):
            os.remove(posix_path)
            return True
        elif os.path.isdir(posix_path):
            shutil.rmtree(posix_path)
            return True
        else:
            raise DirectOperationFailed(
                'Target path {} was neither a file nor a directory'.format(
                    path_to_delete))
    except Exception as err:
        if permissive:
            return False
        else:
            raise DirectOperationFailed(
                'Exception encountered removing target path', err)


def rename(path_to_rename,
           new_path_name,
           system_id=DEFAULT_SYSTEM_ID,
           force=False,
           runtime=None,
           root_dir='/',
           permissive=False,
           agave=None):
    """Emulate Tapis files-rename via rename() on the local host

    Args:
        path_to_rename (str): Path on the storageSystem to move
        new_path_name (str): destination on the storageSystem
        system_id (str, optional): Tapis storageSystem to act upon
        force (bool, optional): Force overwrite of an existing file or directory
        runtime (str, optional): Override the detected Bacanora runtime
        root_dir (str, optional): Base directory if path_to_rename and new_path_name are relative
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        bool: True on success, False on failure if permissive=True

    Raises:
        HTTPError: Underlying transport or web service error was encountered
       DirectOperationFailed: Some other error was encountered
    """
    try:
        posix_path_1 = abs_path(
            path_to_rename,
            system_id=system_id,
            root_dir=root_dir,
            runtime=runtime,
            agave=agave)
        posix_path_2 = abs_path(
            new_path_name,
            system_id=system_id,
            root_dir=root_dir,
            runtime=runtime,
            agave=agave)
        if os.path.exists(posix_path_2):
            if force:
                delete(
                    new_path_name,
                    system_id=system_id,
                    force=True,
                    runtime=runtime,
                    root_dir=root_dir,
                    agave=agave)
            else:
                raise DirectOperationFailed(
                    'Destination {} exists. Repeat with force=True to overwrite.'
                    .format(new_path_name))

        logger.debug('rename: {} => {}'.format(posix_path_1, posix_path_2))
        os.rename(posix_path_1, posix_path_2)
        return True
    except Exception as err:
        if permissive:
            return False
        else:
            raise DirectOperationFailed(
                'Exception encountered renaming target path', err)


def move(path_to_move,
         destination_path,
         system_id=DEFAULT_SYSTEM_ID,
         force=False,
         runtime=None,
         root_dir='/',
         permissive=False,
         agave=None):
    """Facade for direct.rename()

    Args:
        path_to_move (str): Path on the storageSystem to move
        destination_path (str): destination on the storageSystem
        system_id (str, optional): Tapis storageSystem to act upon
        force (bool, optional): Force overwrite of an existing file or directory
        runtime (str, optional): Override the detected Bacanora runtime
        root_dir (str, optional): Base directory if path_to_move and destination_path are relative
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        bool: True on success, False on failure if permissive=True

    Raises:
        HTTPError: Underlying transport or web service error was encountered
        DirectOperationFailed: Some other error was encountered
    """
    return rename(
        path_to_move,
        destination_path,
        system_id=system_id,
        force=force,
        runtime=runtime,
        root_dir=root_dir,
        permissive=permissive,
        agave=agave)


def copy(path_to_copy,
         destination_path,
         system_id=DEFAULT_SYSTEM_ID,
         force=False,
         runtime=None,
         root_dir='/',
         permissive=False,
         agave=None):
    """Emulate Tapis files-copy via os.copy() and shutil.copytree() on
    the local host

    Args:
        path_to_copy (str): Path on the storageSystem to move
        destination_path (str): destination on the storageSystem
        system_id (str, optional): Tapis storageSystem to act upon
        force (bool, optional): Force overwrite of an existing file or directory
        runtime (str, optional): Override the detected Bacanora runtime
        root_dir (str, optional): Base directory if path_to_copy and destination_path are relative
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        bool: True on success, False on failure if permissive=True

    Raises:
        HTTPError: Underlying transport or web service error was encountered
        DirectOperationFailed: Some other error was encountered
    """
    try:
        posix_path_1 = abs_path(
            path_to_copy,
            system_id=system_id,
            root_dir=root_dir,
            runtime=runtime,
            agave=agave)
        posix_path_2 = abs_path(
            destination_path,
            system_id=system_id,
            root_dir=root_dir,
            runtime=runtime,
            agave=agave)
        if os.path.exists(posix_path_2):
            if force:
                delete(
                    destination_path,
                    system_id=system_id,
                    force=True,
                    runtime=runtime,
                    root_dir=root_dir,
                    agave=agave)
            else:
                raise DirectOperationFailed(
                    'Destination {} exists. Repeat with force=True to overwrite.'
                    .format(destination_path))

        logger.debug('copy: {} => {}'.format(posix_path_1, posix_path_2))

        # TODO - Sanity check destination as well
        if os.path.isfile(posix_path_1):
            shutil.copy2(posix_path_1, posix_path_2, follow_symlinks=True)
            return True
        elif os.path.isdir(posix_path_1):
            shutil.copytree(posix_path_1, posix_path_2, symlinks=True)
            return True
    except Exception as err:
        if permissive:
            return False
        else:
            raise DirectOperationFailed(
                'Exception encountered copying {} to {}'.format(
                    path_to_copy, destination_path), err)

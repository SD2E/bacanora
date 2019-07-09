"""POSIX implementations of ``listdir`` or ``walk`` operations
"""
import os
import shutil
from ..utils import nanoseconds, microseconds, normalize, normpath, rooted_path
from .. import logger as loggermodule
from .. import settings
from .utils import abs_path, abspath_to_tapis
from ..stores import ManagedStoreError
from .exceptions import DirectOperationFailed

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['walk', 'listdir']


def walk(directory_path,
         system_id=DEFAULT_SYSTEM_ID,
         root_dir='/',
         directories=False,
         dotfiles=False,
         agave=None):
    """Recursively list contents of a Tapis files directory.

    Arguments:
        directory_path (str): Full or relative path of directory to walk
        system_id (str, optional): Tapis storageSystem for directory_path
        root_dir (str, optional): Base path if directory_path is relative
        directories (bool, optional): Whether result should include directories
        dotfiles (bool, optional): Whether result should include dotfiles
        permissive (bool, optional): Whether to return False or raise Exception on error
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        list: List of Tapis-canonical absolute paths

    Raises:
        DirectOperationFailed: An exception or error happened
    """
    try:
        directory_path = rooted_path(directory_path, root_dir)
        logger.debug('walk: {}'.format(directory_path))
        posix_path = abs_path(
            directory_path,
            system_id=system_id,
            root_dir=root_dir,
            agave=agave)
        logger.debug('posix_path: {}'.format(posix_path))
        # Sanity checks
        if not os.path.exists(posix_path):
            raise FileNotFoundError(
                'No such file or directory: {}'.format(posix_path))
        if not os.path.isdir(posix_path):
            raise NotADirectoryError('Not a directory: {}'.format(posix_path))
        # Do the os.walk() operation
        found_paths = list()
        for root, _, filenames in os.walk(posix_path):
            for filename in filenames:
                if not filename.startswith('.') or dotfiles:
                    found_paths.append(os.path.join(root, filename))
            if directories and root not in found_paths:
                found_paths.append(root)

        dir_listing = [
            abspath_to_tapis(l, system_id=system_id, agave=agave)
            for l in found_paths
        ]
        logger.debug('walk.result: {} paths'.format(len(dir_listing)))
        return dir_listing

    except Exception as exc:
        raise DirectOperationFailed('Unable to complete os.walk()', exc)


def listdir(directory_path,
            system_id=DEFAULT_SYSTEM_ID,
            root_dir='/',
            directories=True,
            dotfiles=False,
            agave=None):
    """List immediate contents of a Tapis files directory.

    Arguments:
        directory_path (str): Full or relative path of directory to walk
        system_id (str, optional): Tapis storageSystem for directory_path
        root_dir (str, optional): Base path if directory_path is relative
        directories (bool, optional): Whether result should include directories
        dotfiles (bool, optional): Whether result should include dotfiles
        permissive (bool, optional): Whether to return False or raise Exception on error
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        list: List of paths relative to directory_path

    Raises:
        DirectOperationFailed: An exception or error happened
    """
    try:
        directory_path = rooted_path(directory_path, root_dir)
        logger.debug('listdir: {}'.format(directory_path))
        # NOTE - os.walk() will add overhead when contents are nested
        walk_resp = walk(
            directory_path,
            system_id=system_id,
            root_dir=root_dir,
            directories=directories,
            dotfiles=dotfiles,
            agave=agave)
        # Prevents resulting path names from beginning with "/"
        if not directory_path.endswith('/'):
            filter_directory_path = directory_path + '/'
        else:
            filter_directory_path = directory_path
        logger.debug('filter_directory_path: {}'.format(filter_directory_path))

        dir_listing = [
            f.replace(filter_directory_path, '') for f in walk_resp
            if os.path.dirname(f) == directory_path
        ]
        logger.debug('listdir.result: {} paths'.format(len(dir_listing)))

        return dir_listing

    except Exception as exc:
        raise DirectOperationFailed('Unable to complete os.walk()', exc)

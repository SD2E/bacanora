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


def walk(file_path,
         system_id=DEFAULT_SYSTEM_ID,
         root_dir='/',
         directories=False,
         dotfiles=False,
         agave=None):
    try:
        file_path = rooted_path(file_path, root_dir)
        logger.debug('walk: {}'.format(file_path))
        posix_path = abs_path(
            file_path, system_id=system_id, root_dir=root_dir, agave=agave)
        logger.debug('posix_path: {}'.format(posix_path))
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
        return dir_listing

    except Exception as exc:
        raise DirectOperationFailed('Unable to complete os.walk()', exc)
    pass


def listdir(file_path,
            system_id=DEFAULT_SYSTEM_ID,
            root_dir='/',
            directories=True,
            dotfiles=False,
            agave=None):
    file_path = rooted_path(file_path, root_dir)
    logger.debug('listdir: {}'.format(file_path))
    walk_resp = walk(
        file_path,
        system_id=system_id,
        root_dir=root_dir,
        directories=directories,
        dotfiles=dotfiles,
        agave=agave)
    if not file_path.endswith('/'):
        filter_file_path = file_path + '/'
    else:
        filter_file_path = file_path
    logger.debug('filter_file_path: {}'.format(filter_file_path))

    dir_listing = [
        f.replace(filter_file_path, '') for f in walk_resp
        if os.path.dirname(f) == file_path
    ]
    return dir_listing

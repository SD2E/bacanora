import os
import shutil
from ..utils import nanoseconds, microseconds, normalize, normpath
from .. import logger as loggermodule
from .. import settings
from .utils import abs_path
from ..stores import ManagedStoreError
from .exceptions import DirectOperationFailed

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['mkdir', 'delete', 'rename']


def mkdir(path_to_make,
          system_id=DEFAULT_SYSTEM_ID,
          permissive=False,
          agave=None):
    """Emulate Tapis files-mkdir via makedirs() on the local host
    """
    try:
        posix_path = abs_path(path_to_make, system_id=system_id, agave=agave)
        logger.debug('mkdir: {}'.format(posix_path))
        os.makedirs(posix_path, exist_ok=True)
        return True
    except Exception:
        if permissive:
            return False
        else:
            raise DirectOperationFailed(
                'Exception encountered with os.makedirs()')


def delete(path_to_delete,
           system_id=DEFAULT_SYSTEM_ID,
           recursive=True,
           permissive=False,
           agave=None):
    """Emulate Tapis files-delete via remove() or rmtree() on the local host
    """
    try:
        posix_path = abs_path(path_to_delete, system_id=system_id, agave=agave)
        logger.debug('delete: {}'.format(posix_path))

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
    except Exception:
        if permissive:
            return False
        else:
            raise DirectOperationFailed(
                'Exception encountered removing target path')


def rename(path_to_rename,
           new_path_name,
           system_id=DEFAULT_SYSTEM_ID,
           permissive=False,
           agave=None):
    """Emulate Tapis files-rename via rename() on the local host
    """
    try:
        posix_path_1 = abs_path(
            path_to_rename, system_id=system_id, agave=agave)
        posix_path_2 = abs_path(
            new_path_name, system_id=system_id, agave=agave)
        logger.debug('rename: {} => {}'.format(posix_path_1, posix_path_2))
        os.rename(posix_path_1, posix_path_2)
        return True
    except Exception:
        if permissive:
            return False
        else:
            raise DirectOperationFailed(
                'Exception encountered renaming target path')

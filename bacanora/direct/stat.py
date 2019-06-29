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

__all__ = ['exists', 'isfile', 'isdir', 'islink', 'ismount']


def exists(file_path, system_id=DEFAULT_SYSTEM_ID, root_dir='/', agave=None):
    try:
        posix_path = abs_path(
            file_path, system_id=system_id, root_dir=root_dir, agave=agave)
        logger.debug('exists: {}'.format(posix_path))
        if os.path.exists(posix_path):
            return True
        else:
            return False
    except Exception as exc:
        raise DirectOperationFailed('Unable to complete os.path.exists()', exc)


def isfile(file_path, system_id=DEFAULT_SYSTEM_ID, root_dir='/', agave=None):
    try:
        posix_path = abs_path(
            file_path, system_id=system_id, root_dir=root_dir, agave=agave)
        logger.debug('isfile: {}'.format(posix_path))
        if os.path.isfile(posix_path):
            return True
        else:
            return False
    except Exception as exc:
        raise DirectOperationFailed('Unable to complete os.path.isfile()', exc)


def isdir(file_path, system_id=DEFAULT_SYSTEM_ID, root_dir='/', agave=None):
    posix_path = abs_path(
        file_path, system_id=system_id, root_dir=root_dir, agave=agave)
    logger.debug('isdir: {}'.format(posix_path))
    try:
        if os.path.isdir(posix_path):
            return True
        else:
            return False
    except Exception:
        raise DirectOperationFailed('Unable to complete os.path.isdir()')


def islink(file_path, system_id=DEFAULT_SYSTEM_ID, root_dir='/', agave=None):
    posix_path = abs_path(
        file_path, system_id=system_id, root_dir=root_dir, agave=agave)
    try:
        if os.path.islink(posix_path):
            return True
        else:
            return False
    except Exception:
        raise DirectOperationFailed('Unable to complete os.path.islink()')


def ismount(file_path, system_id=DEFAULT_SYSTEM_ID, root_dir='/', agave=None):
    posix_path = abs_path(
        file_path, system_id=system_id, root_dir=root_dir, agave=agave)
    try:
        if os.path.ismount(posix_path):
            return True
        else:
            return False
    except Exception:
        raise DirectOperationFailed('Unable to complete os.path.ismount()')

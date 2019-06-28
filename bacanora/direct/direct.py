import os
import datetime
import shutil
from ..stores import StorageSystem
from .. import runtimes
from .. import logger as loggermodule
from ..utils import *
from .operations import *

logger = loggermodule.get_logger(__name__)


def abs_path(file_path, system_id='data-sd2e-community', agave=None):
    logger.debug('file_path: {}'.format(file_path))
    environ = runtimes.detect()
    s = StorageSystem(system_id, agave=agave)
    return s.runtime_dir(environ, file_path)


def mkdir(path_to_make, system_id='data-sd2e-community'):
    full_dest_path = abs_path(path_to_make)
    try:
        os.makedirs(full_dest_path)
        return True
    except Exception:
        raise DirectOperationFailed('Exception encountered with os.makedirs()')


def delete(path_to_rm, system_id='data-sd2e-community', recursive=True):
    full_dest_path = abs_path(path_to_rm)
    try:
        if os.path.isfile(full_dest_path):
            os.remove(full_dest_path)
            return True
        elif os.path.isdir(full_dest_path):
            shutil.rmtree(full_dest_path)
            return True
        else:
            raise ValueError(
                'path {} is not a file or directory'.format(path_to_rm))
    except Exception:
        raise DirectOperationFailed('Exception encountered removing path')

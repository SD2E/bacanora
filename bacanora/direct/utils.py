import os
import datetime
import shutil
from ..stores import StorageSystem
from .. import runtimes
from .. import logger as loggermodule

logger = loggermodule.get_logger(__name__)


def abs_path(file_path, system_id='data-sd2e-community', agave=None):
    logger.debug('file_path: {}'.format(file_path))
    environ = runtimes.detect()
    s = StorageSystem(system_id, agave=agave)
    return s.runtime_dir(environ, file_path)

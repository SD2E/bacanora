import os
import datetime
import shutil
from ..stores import StorageSystem
from .. import runtimes
from .. import logger as loggermodule
from ..utils import normalize

logger = loggermodule.get_logger(__name__)


def abs_path(file_path,
             system_id='data-sd2e-community',
             root_dir='/',
             agave=None):
    file_path = os.path.join(root_dir, normalize(file_path))
    logger.debug('file_path: {}'.format(file_path))
    environ = runtimes.detect()
    s = StorageSystem(system_id, agave=agave)
    file_abs_path = s.runtime_dir(environ, file_path)
    logger.debug('abs_path: {}'.format(file_abs_path))
    return file_abs_path

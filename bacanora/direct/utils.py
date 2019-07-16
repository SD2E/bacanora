"""Provides utilities for path manipulation, etc.
"""
import os
import datetime
import shutil
from ..stores import StorageSystem
from .. import runtimes
from .. import logger as loggermodule
from ..utils import normalize

logger = loggermodule.get_logger(__name__)

__all__ = ['abs_path', 'abspath_to_tapis']


def abs_path(file_path,
             system_id='data-sd2e-community',
             root_dir='/',
             runtime=None,
             agave=None):
    """Resolve an Tapis-relative path to its absolute path on a TACC
    data-enabled host. Automatically detects common TACC host runtimes.

    Arguments:
        file_path (str): File path to resolve
        system_id (str, optional): Tapis storageSystem where file_path is located
        root_dir (str, optional): Absolute path if file_path is relative
        runtime (str, optional): Override detected Bacanora runtime
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        str: Absolute path on the TACC data-enabled host
    """
    detected_runtime = runtimes.detect(override=runtime)
    file_path = os.path.join(root_dir, normalize(file_path))
    logger.debug('file_path: {}'.format(file_path))
    s = StorageSystem(system_id, agave=agave)
    file_abs_path = s.runtime_dir(detected_runtime, file_path)
    logger.debug('abs_path: {}'.format(file_abs_path))
    return file_abs_path


def abspath_to_tapis(file_path,
                     system_id='data-sd2e-community',
                     root_dir='/',
                     runtime=None,
                     agave=None):
    """Resolve a POSIX absolute path on a TACC data-enabled host to its most
    likely Tapis storageSystem equivalient. Automatically detects common
    TACC host runtimes.

    Arguments:
        file_path (str): File path to resolve
        system_id (str, optional): Tapis storageSystem for file_path is located
        root_dir (str, optional): Absolute path if file_path is relative
        runtime (str, optional): Override detected Bacanora runtime
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        str:  Absolute path on the Tapis storageSystem
    """
    detected_runtime = runtimes.detect(override=runtime)
    file_path = os.path.join(root_dir, normalize(file_path))
    logger.debug('file_path: {}'.format(file_path))
    s = StorageSystem(system_id, agave=agave)
    base_path = s.runtime_dir(detected_runtime, '/')
    logger.debug('base_path: {}'.format(base_path))
    tapis_path = file_path.replace(base_path, '/')
    logger.debug('tapis_path: {}'.format(tapis_path))
    return tapis_path

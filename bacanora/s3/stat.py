"""S3-oriented implementations of ``stat`` operations
"""

import os
import shutil
from ..utils import nanoseconds, microseconds, normalize, normpath, rooted_path
from ..logger import get_logger
from .. import runtimes
from .. import settings
from .bucket import system_props_from_bucket
from .exceptions import S3OperationFailed, UnknowableOutcome
from .system import (corral_base_from_runtime, s3_src_dir_from_system,
                     corral_base_from_runtime)

logger = get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['abs_path', 'exists', 'bucket_exists', 'isfile', 'isdir']


def abs_path(bucket_name, bucket_path, root_dir='/', runtime=None, agave=None):
    """Resolve POSIX path on a TACC data-enabled host for an S3 resource

    Arguments:
        bucket_name (str): A TACC S3 bucket
        bucket_path (str): Path within the bucket
        root_dir (str, optional): Base path if bucket_path is relative
        runtime (str, optional): Override detected Bacanora runtime
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        str: Absolute path on the TACC data-enabled host
    """
    detected_runtime = runtimes.detect(override=runtime)
    rooted_bucket_path = rooted_path(bucket_path, root_dir)
    corral_base = corral_base_from_runtime(runtime=detected_runtime)
    (system_id, system_root, system_type,
     system_shortname) = system_props_from_bucket(bucket_name)
    src_dir = s3_src_dir_from_system(system_id)
    result = normpath(
        os.path.join(
            normalize(corral_base), normalize(src_dir),
            normalize(rooted_bucket_path)))
    return result


def exists(bucket_name,
           bucket_path,
           root_dir='/',
           runtime=None,
           permissive=False,
           agave=None):
    """Test for existence of TACC S3 resource

    Arguments:
        bucket_name (str): A TACC S3 bucket
        bucket_path (str): Path within the bucket
        root_dir (str, optional): Base path if bucket_path is relative
        runtime (str, optional): Override detected Bacanora runtime
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        bool: True if path exists and False if not
    """
    try:
        posix_path = abs_path(
            bucket_name,
            bucket_path,
            runtime=runtime,
            root_dir=root_dir,
            agave=agave)
        logger.info('exists({})'.format(posix_path))
        if os.path.exists(posix_path):
            logger.debug('exists({}): True'.format(posix_path))
            return True
        else:
            logger.debug('exists({}): False'.format(posix_path))
    except Exception as exc:
        raise S3OperationFailed('Unable to complete os.path.exists()', exc)


def isfile(bucket_name,
           bucket_path,
           root_dir='/',
           runtime=None,
           permissive=False,
           agave=None):
    """Test if S3 resource points to a file-like object

    Arguments:
        bucket_name (str): A TACC S3 bucket
        bucket_path (str): Path within the bucket
        root_dir (str, optional): Base path if bucket_path is relative
        runtime (str, optional): Override detected Bacanora runtime
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        bool: True if path is a file, and False if not
    """
    try:
        posix_path = abs_path(
            bucket_name,
            bucket_path,
            runtime=runtime,
            root_dir=root_dir,
            agave=agave)
        logger.info('exists({})'.format(posix_path))
        if os.path.isfile(posix_path):
            logger.debug('exists({}): True'.format(posix_path))
            return True
        else:
            logger.debug('exists({}): False'.format(posix_path))
    except Exception as exc:
        raise S3OperationFailed('Unable to complete os.path.exists()', exc)


def isdir(bucket_name,
          bucket_path,
          root_dir='/',
          runtime=None,
          permissive=False,
          agave=None):
    """Test if S3 resource points to a directory-like object

    Arguments:
        bucket_name (str): A TACC S3 bucket
        bucket_path (str): Path within the bucket
        root_dir (str, optional): Base path if bucket_path is relative
        runtime (str, optional): Override detected Bacanora runtime
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        bool: True if path is a directory, and False if not
    """
    try:
        posix_path = abs_path(
            bucket_name,
            bucket_path,
            runtime=runtime,
            root_dir=root_dir,
            agave=agave)
        logger.info('exists({})'.format(posix_path))
        if os.path.isdir(posix_path):
            logger.debug('exists({}): True'.format(posix_path))
            return True
        else:
            logger.debug('exists({}): False'.format(posix_path))
    except Exception as exc:
        raise S3OperationFailed('Unable to complete os.path.exists()', exc)


def bucket_exists(bucket_name, runtime=None, permissive=False, agave=None):
    """Test for existence of TACC S3 bucket

    Arguments:
        bucket_name (str): A TACC S3 bucket
        runtime (str, optional): Override detected Bacanora runtime
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        bool: True if bucket exists and False if not
    """
    return exists(
        bucket_name, '', runtime=runtime, permissive=permissive, agave=agave)

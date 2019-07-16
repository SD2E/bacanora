"""Direct POSIX operations for syncing data from S3 to Tapis storage
"""
import os
import shutil
from .bucket import s3_to_tapis
from .system import s3_runtime_paths, runtimes
from .exceptions import S3OperationFailed
from ..logger import get_logger
from ..tapis import to_agave_uri
from ..utils import nanoseconds
logger = get_logger(__name__)

__all__ = ['import_file']


def import_file(bucket_name,
                bucket_path,
                force=False,
                runtime=None,
                permissive=False,
                profile=False,
                agave=None):
    """Copy a file uploaded to a TACC S3 bucket with its
    corresponding Tapis storageSystem

    Arguments:
        bucket_name (str): TACC S3 bucket name
        bucket_path (str): Absolute path on the bucket
        force (bool, optional): Force the copy even if files do not differ
        runtime (str, optional): Which Bacanora runtime to use for resolving paths
        permissive (bool, optional): Whether to raise an Exception on error
        agave (Agave, optional): An active Tapis API client

    Returns:
        str: Agave-canonical files URI for the copied file

    Raises:
        S3OperationFailed: The copy was attempted but did not succeed
    """

    # logger.info('sync: s3 -- {} {}'.format(bucket_name, bucket_path))
    (system_id, system_path) = s3_to_tapis(bucket_name, bucket_path)
    # logger.debug('sync: tapis -- {} {}'.format(system_id, system_path))

    s3_posix_src, tapis_posix_dest = s3_runtime_paths(
        system_path, system_id, runtime=runtime, agave=agave)
    logger.debug('sync: src={}'.format(s3_posix_src))
    logger.debug('sync: dest={}'.format(tapis_posix_dest))
    start_time = nanoseconds()
    if force or cmpfiles(s3_posix_src, tapis_posix_dest) is False:
        # Do POSIX copy with forced overwrite
        if os.path.isfile(s3_posix_src):
            try:
                shutil.copy(s3_posix_src, tapis_posix_dest)
                elapsed_sec = (nanoseconds() - start_time) / (
                    1000 * 1000 * 1000)
                if profile:
                    logger.info(
                        'import_file.shutil.copy(): {}s elapsed'.format(
                            elapsed_sec))
                return to_agave_uri(system_id, system_path)
            except Exception as exc:
                raise S3OperationFailed('Failed to sync {}: {}'.format(
                    bucket_path, exc))


def cmpfiles(posix_src,
             posix_dest,
             files_only=False,
             mtime=False,
             size=True,
             cksum=False):
    """Check whether two POSIX paths exist and are the same

    Arguments:
        posix_src (str): Path to first file
        posix_dest (str): Path to second file
        files_only (bool, optional): Whether to compare directories
        mtime (bool, optional): Compare modification times
        size (bool, optional): Compare sizes
        cksum (bool, optional): Compare checksums (not implemented)

    Returns:
        bool: True if files are identical, False if not
    """

    # Check existence
    if not os.path.exists(posix_dest):
        logger.debug('Path: destination=absent')
        return False

    if not os.path.exists(posix_src):
        logger.debug('Path: source=absent')
        return False

    if files_only:
        if not os.path.file(posix_src) and not os.path.isfile(posix_dest):
            return True

    # Both files exist, so read in POSIX stat
    stat_src = os.stat(posix_src)
    stat_dest = os.stat(posix_dest)

    # Modification time (conditional)
    if mtime:
        # Mtime on source should never be more recent than
        # destination, as destination is a result of a copy
        # operation. We might need to add ability to account
        # for clock skew but at present we assume source and
        # destination filesystems are managed by the same host
        if stat_src.st_mtime > stat_dest.st_mtime:
            logger.debug('Path: source.mtime != destination.mtime')
            return False
    # Size (conditional)
    if size:
        if stat_src.st_size != stat_dest.st_size:
            logger.debug('Path: source.size != destination.size')
            return False
    if cksum:
        # Not implemented
        # TODO Implement very fast hasher instead of sha256 for sync
        #      1. https://github.com/kalafut/py-imohash
        #      2. https://pypi.org/project/xxhash/
        raise NotImplementedError('Checksum comparison is not yet implemented')

    # None of the False tests returned so we can safely return True
    return True

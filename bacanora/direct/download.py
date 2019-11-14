"""Provides Tapis ``files-get`` operations
"""
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

__all__ = ['get']


def get(file_path,
        system_id=DEFAULT_SYSTEM_ID,
        root_dir='/',
        local_filename=None,
        force=False,
        runtime=None,
        atomic=False,
        permissive=False,
        agave=None):
    """Emulate a Tapis download by copying a path from its resolved physical
    location to the local host

    Arguments:
        file_path (str): Path on the storageSystem to download
        system_id (str, optional): Tapis storageSystem to act upon
        root_dir (str, optional): Base path if file_path is relative
        local_filename (str, optional): Local name of downloaded file
        force (bool, optional): Force overwrite of an existing file or directory
        runtime (str, optional): Override detected Bacanora runtime
        atomic (bool, optional): Whether to download first to a temporary file
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        str: Name of the downloaded file

    Raises:
        DirectOperationFailed: Some other error was encountered
    """
    posix_path = abs_path(
        file_path,
        system_id=system_id,
        runtime=runtime,
        root_dir=root_dir,
        agave=agave)
    try:
        if local_filename is None:
            local_filename = os.path.basename(posix_path)
        if os.path.exists(local_filename) and force is False:
            raise DirectOperationFailed(
                'Destination file {} exists. Repeat with force=True to overwrite.'
            )
        local_parent_dir = normpath(os.path.dirname(local_filename))
        logger.debug('get: {}'.format(posix_path))

        # Stage download to filename-TIMESTAMP then rename into place
        if atomic:
            temp_fname = local_filename + '-' + str(nanoseconds)
        else:
            temp_fname = local_filename

        # Create local destination dir if needed
        if local_parent_dir != '':
            if not os.path.exists(local_parent_dir):
                try:
                    logger.debug('makedirs: {}'.format(local_parent_dir))
                    os.makedirs(local_parent_dir, exist_ok=True)
                except Exception as exc:
                    raise DirectOperationFailed(
                        'Unable to create destination {}'.format(
                            local_parent_dir), exc)

        # Do the download
        if os.path.exists(posix_path):
            try:
                shutil.copy(posix_path, temp_fname)
            except Exception as exc:
                raise DirectOperationFailed(
                    'Copy failed: {}'.format(posix_path), exc)
        else:
            raise DirectOperationFailed(
                'Source does not exist: {}'.format(posix_path))

        # Rename or copy the tempfile into place
        if atomic:
            try:
                if settings.DEBUG_MODE is False:
                    os.rename(temp_fname, local_filename)
                else:
                    logger.debug('temp filename: {}'.format(temp_fname))
                    shutil.copy(temp_fname, local_filename)
            except Exception as rexc:
                raise DirectOperationFailed('Rename failed after download',
                                            rexc)
    except ManagedStoreError as uexc:
        raise DirectOperationFailed(uexc)

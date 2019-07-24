"""Provides Tapis ``files-upload`` operations
"""
import os
import shutil
from ..utils import (nanoseconds, microseconds, normalize, normpath,
                     rooted_path)
from .. import logger as loggermodule
from .. import settings
from .utils import abs_path
from ..stores import ManagedStoreError
from .exceptions import DirectOperationFailed

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM
ATOMIC_OPS = settings.FILES_ATOMIC_OPERATIONS

__all__ = ['put']


def put(file_to_upload,
        destination_path,
        system_id=DEFAULT_SYSTEM_ID,
        root_dir='/',
        runtime=None,
        force=False,
        sync=False,
        atomic=True,
        permissive=False,
        agave=None):
    """Emulate a Tapis files-upload by copying a file to its physical
    location on the local host. Offers an atomic operations option.

    Arguments:
        file_to_upload (str): Name or relative path of file to upload
        destination_path (str): Upload destination on Tapis storageSystem
        system_id (str, optional): Tapis storageSystem where upload will go
        root_dir (str, optional): Base path if destination_path is relative
        runtime (str, optional): Override detected Bacanora runtime
        force (bool, optional): Force overwrite on storageSystem
        atomic (bool, optional): Whether to upload first to a temporary file
        sync (bool, optional): Wait until the file uploads to return
        permissive (bool, optional): Whether to return False or raise Exception on error
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        bool: True on success and False on failure

    Raises:
        DirectOperationFailed: An exception or error happened
    """
    try:
        # TODO - implement sync (just a facade since direct IO is blocking)
        # DONE - implement atomic upload
        # TODO - implement force for remote overwrites
        try:
            file_name = os.path.basename(file_to_upload)
            posix_path = abs_path(
                rooted_path(destination_path, root_dir),
                system_id=system_id,
                runtime=runtime,
                agave=agave)
            logger.debug('put: {} => {}'.format(file_name, posix_path))
            # Ensure remote destination path exists. Tapis files does this
            # automatically on upload but POSIX does not. This is gated behind
            # the force keyword argument.
            if force:
                try:
                    for pp in (os.path.dirname(posix_path), posix_path):
                        logger.debug('makedirs: {}'.format(pp))
                        os.makedirs(pp, exist_ok=True)
                except Exception as exc:
                    raise DirectOperationFailed(
                        'Unable to create destination {}'.format(posix_path),
                        exc)

            # Stage upload to filename-TIMESTAMP then rename into place
            if atomic:
                temp_fname = file_to_upload + '-' + str(nanoseconds())
            else:
                temp_fname = file_to_upload
            temp_fname = os.path.basename(temp_fname)

            # Do the upload
            try:
                shutil.copy(file_to_upload, os.path.join(
                    posix_path, temp_fname))
            except Exception as exc:
                raise DirectOperationFailed(
                    'Copy {} failed'.format(temp_fname), exc)

            # Rename or copy the tempfile into place
            if atomic:
                try:
                    if settings.DEBUG_MODE is False:
                        os.rename(
                            os.path.join(posix_path, temp_fname),
                            os.path.join(posix_path,
                                         os.path.basename(file_to_upload)))
                    else:
                        logger.debug('temp filename: {}'.format(temp_fname))
                        shutil.copy(
                            os.path.join(posix_path, temp_fname),
                            os.path.join(posix_path,
                                         os.path.basename(file_to_upload)))
                except Exception as rexc:
                    raise DirectOperationFailed('Rename failed after upload',
                                                rexc)
        except ManagedStoreError as uexc:
            raise DirectOperationFailed(uexc)
    except Exception:
        if permissive:
            return False
        else:
            raise

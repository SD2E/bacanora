"""POSIX implementations of Tapis ``files-get`` operations
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
        local_filename=None,
        force=False,
        atomic=True,
        agave=None):
    """Emulate a Tapis download by copying a path from its resolved physical
    location to the local host
    """
    try:
        posix_path = abs_path(file_path, system_id=system_id, agave=agave)
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
                raise DirectOperationFailed('Copy failed', exc)
        else:
            raise DirectOperationFailed('Source does not exist')

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

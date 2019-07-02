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

__all__ = ['put']


def put(file_path,
        destination_dir,
        system_id=DEFAULT_SYSTEM_ID,
        root_dir='/',
        atomic=True,
        permissive=False,
        agave=None):
    """Emulate a Tapis files-upload by copying a file to its physical
    location on the local host

    Arguments:

    Returns:

    Raises:
        DirectOperationFailed:
    """
    try:
        try:
            file_name = os.path.basename(file_path)
            posix_path = abs_path(
                rooted_path(destination_dir, root_dir),
                system_id=system_id,
                agave=agave)
            logger.debug('put: {} => {}'.format(file_name, posix_path))
            # Ensure remote destination path exists. Tapis files does this
            # automatically on upload but POSIX does not
            try:
                for pp in (os.path.dirname(posix_path), posix_path):
                    logger.debug('makedirs: {}'.format(pp))
                    os.makedirs(pp, exist_ok=True)
            except Exception as exc:
                raise DirectOperationFailed(
                    'Unable to create destination {}'.format(posix_path), exc)

            # Stage upload to filename-TIMESTAMP then rename into place
            if atomic:
                temp_fname = file_path + '-' + str(nanoseconds())
            else:
                temp_fname = file_path
            temp_fname = os.path.basename(temp_fname)

            # Do the upload
            try:
                shutil.copy(file_path, os.path.join(posix_path, temp_fname))
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
                                         os.path.basename(file_path)))
                    else:
                        logger.debug('temp filename: {}'.format(temp_fname))
                        shutil.copy(
                            os.path.join(posix_path, temp_fname),
                            os.path.join(posix_path,
                                         os.path.basename(file_path)))
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

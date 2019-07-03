"""Tapis implementations of ``put`` operations
"""
import os
import shutil
from ..logger import get_logger
from .. import settings
from ..utils import nanoseconds, microseconds, normalize, normpath, rooted_path
from .utils import read_tapis_http_error
from ..exceptions import HTTPError, AgaveError
from .exceptions import TapisOperationFailed

logger = get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM
FILES_MAX_SYNC_ELAPSED = settings.MAX_SYNC_ELAPSED_FILES

__all__ = ['put']

# As a hack to fix the issue with in-place overwrites: Upload to a
# namespaced path (agaveDestPath.tmp), track the existence of that file,
# then do a mv operation at the end. Formally, its no different
# for provenance than uploading in place.


def put(file_to_upload,
        destination_path,
        system_id=DEFAULT_SYSTEM_ID,
        root_dir='/',
        force=False,
        atomic=True,
        sync=False,
        permissive=False,
        agave=None):
    """Wrapper for Tapis files-upload with atomic operations and sync mode.

    Arguments:
        file_to_upload (str): Name or relative path of file to upload
        destination_path (str): Upload destination on Tapis storageSystem
        system_id (str, optional): Tapis storageSystem where upload will go
        root_dir (str, optional): Base path if destination_path is relative
        force (bool, optional): Force overwrite on storageSystem
        atomic (bool, optional): Whether to upload first to a temporary file
        sync (bool, optional): Wait until the file uploads to return
        permissive (bool, optional): Whether to return False or raise Exception on error
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        bool: True on success and False on failure

    Raises:
        IOError: The target file could not be read
        OSError: A low-level error happened outside Python
        HTTPError: A transport or web service error was encountered
        TapisOperationFailed: Some other exception or error happened
    """
    try:
        # TODO - implement sync
        # TODO - implement atomic upload
        # TODO - implement force for remote overwrites
        try:
            destination_path = rooted_path(destination_path, root_dir)
            agave.files.importData(
                systemId=system_id,
                filePath=destination_path,
                fileToUpload=open(file_to_upload))
            return True
        except HTTPError as h:
            error_msg = read_tapis_http_error(h)
            logger.error(error_msg)
            raise HTTPError(error_msg)
        except (OSError, IOError) as err:
            logger.error(str(err))
            raise
        except Exception as exc:
            raise TapisOperationFailed("Upload failed: {}".format(exc))
    except Exception:
        if permissive:
            return False
        else:
            raise

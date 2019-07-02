import os
import shutil
from agavepy.agave import AgaveError
from requests.exceptions import HTTPError
from .. import logger as loggermodule
from .. import settings
from ..utils import nanoseconds, microseconds, normalize, normpath, rooted_path
from ..stores import ManagedStoreError
from .exceptions import TapisOperationFailed
from .utils import process_agave_httperror

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM
FILES_MAX_SYNC_ELAPSED = settings.

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
            error_msg = process_agave_httperror(h)
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


def agave_upload_file(agaveClient,
                      agaveDestPath,
                      systemId,
                      uploadFile,
                      sync=True,
                      timeOut=MAX_ELAPSED):
    """
    Upload a file to Agave-managed remote storage.

    If sync is True, the function will wait for the upload to
    complete before returning. Raises exceptions on importData
    or timeout errors.
    """
    # NOTE: I know a hack to fix the issue with in-place overwrites not having
    # the proper terminal state. It should also increase the atomicity of the
    # uploads process. Upload to a namespaced path (agaveDestPath.tmp), track
    # that file, then do a mv operation at the end. Formally, its no differnt
    # for provenance than uploading in place.
    try:
        agaveClient.files.importData(
            systemId=systemId,
            filePath=agaveDestPath,
            fileToUpload=open(uploadFile))
    except HTTPError as h:
        http_err_resp = process_agave_httperror(h)
        raise Exception(http_err_resp)
    except Exception as e:
        raise Exception("Unknown error uploading {}: {}".format(uploadFile, e))

    uploaded_filename = os.path.basename(uploadFile)
    if sync:
        fullAgaveDestPath = os.path.join(agaveDestPath, uploaded_filename)
        wait_for_file_status(agaveClient, fullAgaveDestPath, systemId, timeOut)

    return True

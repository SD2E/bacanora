"""Web service implementations of ``files-upload`` operations
"""
import os
import shutil
import time
from ..logger import get_logger
from .. import settings
from ..utils import nanoseconds, microseconds, normalize, normpath, rooted_path
from .utils import read_tapis_http_error, handle_http_error
from ..exceptions import (AgaveError, HTTPError)
from .exceptions import (HTTPNotFoundError, ImportNotCompleteError,
                         TapisOperationFailed)
from .stat import isdir, stat
from .manage import mkdir, rename
from tenacity import (retry, retry_if_exception_type, stop_after_delay,
                      wait_exponential)

logger = get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM
IMPORT_DATA_MAX_ELAPSED = settings.IMPORT_DATA_MAX_ELAPSED
IMPORT_DATA_MAX_ALLOWED = IMPORT_DATA_MAX_ELAPSED * 4
IMPORT_DATA_RETRY_DELAY = settings.IMPORT_DATA_RETRY_DELAY

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
        atomic=False,
        sync=True,
        permissive=False,
        agave=None,
        **kwargs):
    """Wrapper for Tapis files-upload with atomic operations and sync mode.

    Arguments:
        file_to_upload (str): Name or relative path of file to upload
        destination_path (str): Upload directory on Tapis storageSystem
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
        # We must override user value for "atomic" as it is required
        # for a synchronous operation that we upload using a temp file
        file_name = file_to_upload
        if atomic:
            temp_file_name = file_name + '.part-' + str(nanoseconds())
            shutil.copyfile(file_to_upload, temp_file_name)
        else:
            temp_file_name = file_name
        try:
            destination_path = rooted_path(destination_path, root_dir)
            if force:
                logger.debug('Checking if {} exists'.format(destination_path))
                if not isdir(
                        destination_path,
                        system_id=system_id,
                        root_dir=root_dir,
                        permissive=True,
                        agave=agave):
                    logger.debug(
                        'Nope... creating {}'.format(destination_path))
                    mkdir(
                        destination_path,
                        system_id=system_id,
                        root_dir=root_dir,
                        force=True,
                        agave=agave)
            logger.debug('Starting to import {} to {}'.format(
                temp_file_name, destination_path))
            agave.files.importData(
                systemId=system_id,
                filePath=destination_path,
                fileToUpload=open(temp_file_name, 'rb'))
            if atomic:
                try:
                    os.unlink(temp_file_name)
                except Exception:
                    logger.exception(
                        'Failed to delete local temporary file {}'.format(
                            temp_file_name))
            if sync:
                logger.debug(
                    'Synchronous upload: Waiting on {} to be imported'.format(
                        temp_file_name))
                start_time = nanoseconds()
                check_import(temp_file_name, system_id=system_id, agave=agave)
                elapsed_time = (nanoseconds() - start_time) / (
                    1000 * 1000 * 1000)
                logger.debug('Imported {} in {} seconds'.format(
                    temp_file_name, elapsed_time))
            if atomic:
                logger.debug('Atomic upload: Renaming {} to {}'.format(
                    temp_file_name, file_name))
                rename(
                    temp_file_name,
                    os.path.join(destination_path, file_name),
                    system_id=system_id,
                    force=True,
                    agave=agave)
            # Only returned if there are no exceptions raised
            return True
        except HTTPError as h:
            handle_http_error(h)
            # error_msg = read_tapis_http_error(h)
            # logger.error(error_msg)
            # raise HTTPError(error_msg)
        except (OSError, IOError) as err:
            logger.error(str(err))
            raise
        except Exception as exc:
            raise
            # raise TapisOperationFailed("Upload failed: {}".format(exc))
    except Exception:
        if permissive:
            return False
        else:
            raise


@retry(
    retry=retry_if_exception_type(HTTPError),
    reraise=True,
    stop=stop_after_delay(IMPORT_DATA_MAX_ELAPSED),
    wait=wait_exponential(multiplier=1, min=IMPORT_DATA_RETRY_DELAY, max=32))
def check_import(path_to_monitor,
                 size=-1,
                 system_id=DEFAULT_SYSTEM_ID,
                 root_dir='/',
                 permissive=False,
                 agave=None):

    logger.info('Checking status of {}'.format(path_to_monitor))
    record = dict()
    try:
        record = stat(
            path_to_monitor,
            system_id=system_id,
            root_dir=root_dir,
            permissive=False,
            agave=agave)

    except HTTPNotFoundError:
        raise
    except HTTPError:
        raise

    if size > 0:
        rl = record.get('length', 0)
        if rl <= size:
            logger.warning('Only {} of {} bytes have been uploaded'.format(
                rl, size))
            raise ImportNotCompleteError(
                'Only {} of {} bytes have been uploaded'.format(rl, size))

    return True

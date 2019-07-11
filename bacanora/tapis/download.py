"""Tapis implementations of ``files-get`` operations
"""
import os
import shutil
from .. import logger as loggermodule
from .. import settings
from ..utils import nanoseconds, microseconds, normalize, normpath
from ..exceptions import HTTPError, AgaveError
from .exceptions import TapisOperationFailed
from .utils import read_tapis_http_error

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM
BLOCK_SIZE = settings.FILES_BLOCK_SIZE

__all__ = ['get']


def get(file_path,
        system_id=DEFAULT_SYSTEM_ID,
        local_filename=None,
        force=False,
        atomic=True,
        permissive=False,
        agave=None,
        **kwargs):
    """Wrapper for Tapis files-get, adding atomic operations

    Args:
        file_path (str): Path on the storageSystem to download
        system_id (str, optional): Tapis storageSystem to act upon
        local_filename (str, optional): Local name of downloaded file
        force (bool, optional): Force overwrite of an existing file or directory
        atomic (bool, optional): Whether to download first to a temporary file
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        str: Name of the downloaded file

    Raises:
        HTTPError: Underlying transport or web service error was encountered
        TapisOperationFailed: Some other error was encountered
    """
    try:
        logger.debug('get: {}'.format(file_path))
        if local_filename is None:
            local_filename = os.path.basename(file_path)
        if atomic:
            tmp_local_filename = local_filename + '-' + str(nanoseconds())
        else:
            tmp_local_filename = local_filename
        logger.debug('destination: {}'.format(tmp_local_filename))

        if os.path.exists(local_filename) and force is False:
            raise TapisOperationFailed(
                'Local destination {} exists. Repeat with force=True to overwrite it.'
                .format(local_filename))

        try:
            logger.debug('files.download: agave://{}{}'.format(
                system_id, file_path))
            rsp = agave.files.download(filePath=file_path, systemId=system_id)
            if type(rsp) == dict:
                raise TapisOperationFailed(
                    "Failed to download {}".format(file_path))
            with open(tmp_local_filename, 'wb') as dest_file:
                for block in rsp.iter_content(BLOCK_SIZE):
                    if not block:
                        break
                    dest_file.write(block)
            if atomic:
                try:
                    if settings.DEBUG_MODE is False:
                        os.rename(tmp_local_filename, local_filename)
                    else:
                        logger.debug(
                            'temp filename: {}'.format(tmp_local_filename))
                        shutil.copy(tmp_local_filename, local_filename)
                except Exception as err:
                    raise IOError('Rename failed after download', err)
        except HTTPError as h:
            error_msg = read_tapis_http_error(h)
            logger.error(error_msg)
            raise HTTPError(error_msg)
        except (OSError, IOError) as err:
            logger.error(str(err))
            raise
        except Exception as exc:
            raise TapisOperationFailed("Download failed: {}".format(exc))

        return local_filename

    except Exception:
        if permissive:
            return False
        else:
            raise

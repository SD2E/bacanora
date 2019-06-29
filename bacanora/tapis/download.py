import os
import shutil
from agavepy.agave import AgaveError
from requests.exceptions import HTTPError
from .. import logger as loggermodule
from .. import settings
from ..utils import nanoseconds, microseconds, normalize, normpath
from ..stores import ManagedStoreError
from .exceptions import TapisOperationFailed
from .utils import process_agave_httperror

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM
BLOCK_SIZE = settings.FILES_BLOCK_SIZE


def get(file_path,
        system_id=DEFAULT_SYSTEM_ID,
        local_filename=None,
        atomic=True,
        agave=None):
    """Wrapper for Tapis files-get with atomic operations
    """
    logger.debug('get: {}'.format(file_path))
    if local_filename is None:
        local_filename = os.path.basename(file_path)
    if atomic:
        tmp_local_filename = local_filename + '-' + str(nanoseconds())
    else:
        tmp_local_filename = local_filename
    logger.debug('destination: {}'.format(tmp_local_filename))

    try:
        with open(tmp_local_filename, 'wb') as dest_file:
            logger.debug('files.download: agave://{}{}'.format(
                system_id, file_path))
            rsp = agave.files.download(filePath=file_path, systemId=system_id)
            if type(rsp) == dict:
                raise TapisOperationFailed(
                    "Failed to download {}".format(file_path))
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
        raise HTTPError(process_agave_httperror(h))
    except (OSError, IOError):
        raise
    except Exception as exc:
        raise TapisOperationFailed("Download failed: {}".format(exc))

    return local_filename

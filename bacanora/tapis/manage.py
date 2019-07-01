import os
import shutil
from agavepy.agave import AgaveError
from requests.exceptions import HTTPError
from .. import logger as loggermodule
from .. import settings
from ..utils import nanoseconds, microseconds, normalize, normpath
from ..stores import ManagedStoreError
from .exceptions import TapisOperationFailed
from .utils import process_agave_httperror, rooted_path

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['mkdir', 'delete']


def mkdir(path_to_make,
          system_id=DEFAULT_SYSTEM_ID,
          root_dir='/',
          permissive=False,
          agave=None):
    """Wrapper for Tapis files-mkdir
    """
    try:
        try:
            logger.debug('mkdir: {}'.format(path_to_make))
            path_to_make = normpath(path_to_make)
            agave.files.manage(
                systemId=system_id,
                body={
                    'action': 'mkdir',
                    'path': path_to_make
                },
                filePath=root_dir)
            return True
        except HTTPError as h:
            http_err_resp = process_agave_httperror(h)
            logger.error('HTTP Error: {}'.format(http_err_resp))
            raise HTTPError(http_err_resp)
        except Exception as err:
            raise TapisOperationFailed(
                'Exception encountered with files.manage.mkdir()', err)
    except Exception:
        if permissive:
            return False
        else:
            raise


def delete(path_to_delete,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           recursive=True,
           permissive=False,
           agave=None):
    """Wrapper for Tapis files-delete
    """
    try:
        try:
            rooted_file_path = rooted_path(path_to_delete, root_dir)
            agave.files.delete(filePath=rooted_file_path, systemId=system_id)
            return True
        except HTTPError as herr:
            if herr.response.status_code == 404:
                logger.warning(
                    'HTTP Error: {} was not found'.format(path_to_delete))
                return False
            else:
                raise HTTPError(herr)
        except Exception as err:
            raise TapisOperationFailed(
                'Exception encountered with files.manage.mkdir()', err)
    except Exception:
        if permissive:
            return False
        else:
            raise


def rename():
    pass


def move():
    pass

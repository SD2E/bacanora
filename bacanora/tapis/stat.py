import os
import shutil
from attrdict import AttrDict
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

FILES_FILE_TYPES = ('file')
FILES_DIRECTORY_TYPES = ('dir')
FILES_TYPES = FILES_FILE_TYPES + FILES_DIRECTORY_TYPES

__all__ = ['stat', 'rsrc_type', 'exists', 'isfile', 'isdir']


# TODO - Add a simple TTL cache for stat()
# TODO - Return a tuple modeled on Python os.stat()
def stat(file_path,
         system_id=DEFAULT_SYSTEM_ID,
         root_dir='/',
         permissive=False,
         agave=None):
    try:
        try:
            rooted_file_path = rooted_path(file_path, root_dir)
            resp = agave.files.list(
                filePath=rooted_file_path, systemId=system_id, limit=2)[0]
            return AttrDict(resp)
        except HTTPError:
            raise
        except Exception as err:
            raise TapisOperationFailed(
                'Exception encountered with stat#files.list()', err)
    except Exception as err:
        logger.warning(
            'Exception encountered in rsrc_exists(): {}'.format(err))
        if permissive:
            return dict()
        else:
            raise


def rsrc_type(file_path,
              system_id=DEFAULT_SYSTEM_ID,
              root_dir='/',
              permissive=False,
              agave=None):
    try:
        return stat(
            file_path,
            system_id=system_id,
            root_dir=root_dir,
            permissive=False,
            agave=agave).get('type', None)
    except Exception as err:
        logger.warning('Exception encountered in rsrc_type(): {}'.format(err))
        if permissive:
            return False
        else:
            raise


def exists(file_path,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           permissive=False,
           agave=None):
    """Emulate Python os.path.exists() using agave.files.list()
    """
    try:
        file_path_type = rsrc_type(
            file_path,
            system_id=system_id,
            root_dir=root_dir,
            permissive=False,
            agave=agave)
        return file_path_type in FILES_TYPES
    except HTTPError as herr:
        if herr.response.status_code == 404:
            return False
        else:
            raise HTTPError(herr)
    except Exception as err:
        logger.warning('Exception encountered in exists(): {}'.format(err))
        if permissive:
            return False
        else:
            raise


def isfile(file_path,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           permissive=False,
           agave=None):
    """Emulate Python os.path.isfile() using agave.files.list()
    """
    try:
        file_path_format = rsrc_type(
            file_path,
            system_id=system_id,
            root_dir=root_dir,
            permissive=False,
            agave=agave)
        return file_path_format in FILES_FILE_TYPES
    except Exception as err:
        logger.warning('Exception encountered in isfile(): {}'.format(err))
        if permissive:
            return False
        else:
            raise


def isdir(file_path,
          system_id=DEFAULT_SYSTEM_ID,
          root_dir='/',
          permissive=False,
          agave=None):
    """Emulate Python os.path.isdir() using agave.files.list()
    """
    try:
        file_path_format = rsrc_type(
            file_path,
            system_id=system_id,
            root_dir=root_dir,
            permissive=False,
            agave=agave)
        return file_path_format in FILES_DIRECTORY_TYPES
    except Exception as err:
        logger.warning('Exception encountered in isdir(): {}'.format(err))
        if permissive:
            return False
        else:
            raise


def is_link(file_path,
            system_id=DEFAULT_SYSTEM_ID,
            root_dir='/',
            permissive=False,
            agave=None):
    """Placeholder for a Tapis function to identify links
    """
    raise NotImplementedError(
        'Tapis files is unable to determine if a resource is a link')


def is_mount(file_path,
             system_id=DEFAULT_SYSTEM_ID,
             root_dir='/',
             permissive=False,
             agave=None):
    """Placeholder for a Tapis function to identify mounts
    """
    raise NotImplementedError(
        'Tapis files is unable to determine if a resource is a mount')

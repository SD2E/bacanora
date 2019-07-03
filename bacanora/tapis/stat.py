"""Tapis implementations of ``stat`` operations
"""
import os
import shutil
from attrdict import AttrDict
from .. import logger as loggermodule
from .. import settings
from ..utils import nanoseconds, microseconds, normalize, normpath, rooted_path
from ..exceptions import HTTPError, AgaveError
from .exceptions import TapisOperationFailed
from .utils import read_tapis_http_error

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
    """Retrieve attributes for a given path on a Tapis storageSystem

    Arguments:
        file_path (str): The path from which to fetch attributes
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        dict: A dictionary containing Tapis files API attributes

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
    """
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
    """Retrieve the ``type`` for a given path on a Tapis storageSystem

    Arguments:
        file_path (str): The path from which to fetch attributes
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        string: Either ``file`` or ``dir``

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
    """
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
    """Determine if a path exists on a Tapis storageSystem

    Arguments:
        file_path (str): The path from which to fetch attributes
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path exists and False if not

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
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
    """Determine if a path exists and is a file on a Tapis storageSystem

    Arguments:
        file_path (str): The path from which to fetch attributes
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path is a file and False if not

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
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
    """Determine if a path exists and is a directory on a Tapis storageSystem

    Arguments:
        file_path (str): The path from which to fetch attributes
        system_id (str, optional): The Tapis storageSystem for file_path
        root_dir (str, optional): Base path on the storageSystem if file_path is relative
        permissive (bool, optional): Whether to raise an Exception on failure
        agave (Agave, optional): An active Tapis client

    Returns:
        bool: True if the path is a directory and False if not

    Raises:
        HTTPError: A transport or web services error was encountered
        TapisOperationFailed: Some other error prevented the operation
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
